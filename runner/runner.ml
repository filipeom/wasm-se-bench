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
  OS.Dir.fold_contents
    (fun p acc -> if Fpath.has_ext ".wat" p then p :: acc else acc)
    [] dataset_root

(* TODO: catch errors and return codes of tools *)
let run_single t workspace file =
  let time_start = Unix.gettimeofday () in
  let workspace = Fpath.(workspace // base file) in
  Fmt.pr "Workspace: %a@." Fpath.pp workspace;
  let _ = OS.Dir.create ~path:true workspace in
  let err = OS.Cmd.err_file Fpath.(workspace / "stderr") in
  let stdout = Fpath.(workspace / "stdout") in
  let run_out = OS.Cmd.run_out ~err @@ Tool.cmd t workspace file in
  let _ = OS.Cmd.out_file stdout run_out in
  Unix.gettimeofday () -. time_start

let results_dir = Fpath.v "./results"

let out_results tool dataset results outfile =
  let comma fmt () = Fmt.string fmt "," in
  OS.File.writef outfile "tool,%a@\n%a,%a@."
    (Fmt.list ~sep:comma Fpath.pp)
    dataset Tool.pp tool
    (Fmt.list ~sep:comma Fmt.float)
    results

let result =
  let* dataset = dataset in
  let _ = OS.Dir.create results_dir in
  let wasp_out = Fpath.(results_dir / "wasp") in
  let wasp_res = List.map (run_single wasp wasp_out) dataset in
  let _ = out_results wasp dataset wasp_res Fpath.(wasp_out / "results") in
  let owi_out = Fpath.(results_dir / "owi") in
  let owi_res = List.map (run_single owi owi_out) dataset in
  let _ = out_results owi dataset owi_res Fpath.(owi_out / "results") in
  let owi_out = Fpath.(results_dir / "owi_w20") in
  let owi_res = List.map (run_single owi_w20 owi_out) dataset in
  let _ = out_results owi dataset owi_res Fpath.(owi_out / "results") in
  Ok ()

let () =
  match result with
  | Ok () -> exit 0
  | Error (`Msg msg) ->
      Fmt.epr "%s@." msg;
      exit 1
