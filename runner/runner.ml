open Prelude
open Bos

let ( let* ) = Rresult.R.bind

let owi = Tool.make ~flags:[ "--fail-on-assertion-only" ] Owi

let owi_w20 = Tool.make ~flags:[ "--fail-on-assertion-only" ] ~cpus:20 Owi

let wasp = Tool.make Wasp

let seewasm = Tool.make SeeWasm

let _ = [ owi; owi_w20; wasp; seewasm ]

let wat_dataset_dir = Fpath.v "./datasets/btree/with_ffi"

let wat_dataset =
  let* dataset_root = OS.Dir.must_exist wat_dataset_dir in
  let* dataset =
    OS.Dir.fold_contents
      (fun p acc -> if Fpath.has_ext ".wat" p then p :: acc else acc)
      [] dataset_root
  in
  Ok (List.sort Fpath.compare dataset)

let wasm_dataset_dir = Fpath.v "./datasets/btree/native"

let wasm_dataset =
  let* dataset_root = OS.Dir.must_exist wasm_dataset_dir in
  let* dataset =
    OS.Dir.fold_contents
      (fun p acc -> if Fpath.has_ext ".wasm" p then p :: acc else acc)
      [] dataset_root
  in
  Ok (List.sort Fpath.compare dataset)

let _ = wasm_dataset

(* TODO: catch errors and return codes of tools *)
let run_single t workspace file =
  Fmt.epr "Running %a on %a@." Tool.pp t Fpath.pp (Fpath.base file);
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
  let* _ = wat_dataset in
  let* wasm_dataset = wasm_dataset in
  let _ = OS.Dir.create results_dir in
  (* let wasp_out = Fpath.(results_dir / Tool.to_string wasp) in *)
  (* let wasp_res = List.map (run_single wasp wasp_out) dataset in *)
  (* let owi_out = Fpath.(results_dir / Tool.to_string owi) in *)
  (* let owi_res = List.map (run_single owi owi_out) dataset in *)
  (* let owi_out = Fpath.(results_dir / Tool.to_string owi_w20) in *)
  (* let owi_w20_res = List.map (run_single owi_w20 owi_out) dataset in *)
  (* let table = *)
  (*   [ List.map (fun p -> Fpath.(to_string @@ base p)) dataset *)
  (*   ; List.map string_of_float wasp_res *)
  (*   ; List.map string_of_float owi_res *)
  (*   ; List.map string_of_float owi_w20_res *)
  (*   ] *)
  (* in *)
  let _ = OS.Dir.create Fpath.(v "output" / "log") in
  let seewasm_out = Fpath.(results_dir / Tool.to_string seewasm) in
  let seewasm_res = List.map (run_single seewasm seewasm_out) wasm_dataset in
  let table =
    [ [ Tool.to_string seewasm ] @ List.map string_of_float seewasm_res ]
  in
  Csv.save ~separator:',' Fpath.(to_string (results_dir / "results.csv")) table;
  Ok ()

let () =
  match result with
  | Ok () -> exit 0
  | Error (`Msg msg) ->
      Fmt.epr "%s@." msg;
      exit 1
