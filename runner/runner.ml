open Prelude
open Bos

let ( let* ) = Result.bind

let owi = Tool.make ~flags:[ "--fail-on-assertion-only" ] Owi

let owi_w20 = Tool.make ~flags:[ "--fail-on-assertion-only" ] ~cpus:20 Owi

let wasp = Tool.make Wasp

let _ = [ owi; wasp ]

let dataset_dir = Fpath.v "./datasets/btree/wat"

let dataset =
  let* dataset_root = OS.Dir.must_exist dataset_dir in
  let* dataset =
    OS.Dir.fold_contents
      (fun p acc -> if Fpath.has_ext ".wat" p then p :: acc else acc)
      [] dataset_root
  in
  Ok (List.sort Fpath.compare dataset)

(* TODO: catch errors and return codes of tools *)
let run_single t workspace file =
  Fmt.epr "Running %a on %a@." Tool.pp t Fpath.pp (Fpath.base workspace);
  let time_start = Unix.gettimeofday () in
  let workspace = Fpath.(workspace // base file) in
  let _ = OS.Dir.create ~path:true workspace in
  let err = OS.Cmd.err_file Fpath.(workspace / "stderr") in
  let stdout = Fpath.(workspace / "stdout") in
  let run_out = OS.Cmd.run_out ~err @@ Tool.cmd t workspace file in
  let _ = OS.Cmd.out_file stdout run_out in
  Unix.gettimeofday () -. time_start

let results_dir =
  let t = Unix.localtime (Unix.gettimeofday ()) in
  Fmt.kstr Fpath.v "./results-%d%02d%02d_%02dh%02dm%02ds" (1900 + t.tm_year)
    (1 + t.tm_mon) t.tm_mday t.tm_hour t.tm_min t.tm_sec

let result =
  let* dataset = dataset in
  let _ = OS.Dir.create results_dir in
  let wasp_out = Fpath.(results_dir / "wasp") in
  let wasp_res = List.map (run_single wasp wasp_out) dataset in
  let owi_out = Fpath.(results_dir / "owi") in
  let owi_res = List.map (run_single owi owi_out) dataset in
  let owi_out = Fpath.(results_dir / "owi_w20") in
  let owi_w20_res = List.map (run_single owi_w20 owi_out) dataset in
  let table =
    [ List.map (fun p -> Fpath.(to_string @@ base p)) dataset
    ; List.map string_of_float wasp_res
    ; List.map string_of_float owi_res
    ; List.map string_of_float owi_w20_res
    ]
  in
  Csv.save ~separator:',' Fpath.(to_string (results_dir / "results")) table;
  Ok ()

let () =
  match result with
  | Ok () -> exit 0
  | Error (`Msg msg) ->
      Fmt.epr "%s@." msg;
      exit 1
