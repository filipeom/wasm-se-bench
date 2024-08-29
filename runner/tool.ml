open Bos

type tool_type =
  | Owi
  | Wasp
  | SeeWasm

type t =
  { tool : tool_type
  ; flags : string list
  ; cpus : int
  }

let make ?(flags = []) ?(cpus = 1) tool = { tool; flags; cpus }

let cmd { tool; flags; cpus } workspace file =
  match tool with
  | Owi ->
      Cmd.(
        v "owi"
        % "sym"
        %% of_list flags
        % "-w"
        % string_of_int cpus
        % "--workspace"
        % p workspace
        % p file)
  | Wasp ->
      Cmd.(
        v "wasp"
        % "concolic"
        %% of_list flags
        % "--workspace"
        % p workspace
        % p file)
  | SeeWasm ->
      Cmd.(
        v "python"
        % "tools/SeeWasm/launcher.py"
        % "-f"
        % p file
        % "-s"
        % "--entry"
        % "main")

let pp fmt { tool; cpus; _ } =
  match tool with
  | Owi -> Fmt.pf fmt "owi_w%d" cpus
  | Wasp -> Fmt.string fmt "wasp"
  | SeeWasm -> Fmt.string fmt "seewasm"

let to_string t = Fmt.str "%a" pp t
