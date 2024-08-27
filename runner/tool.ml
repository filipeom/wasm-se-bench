open Bos

type tool_type =
  | Owi
  | Wasp

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

let pp fmt { tool; _ } =
  match tool with Owi -> Fmt.string fmt "owi" | Wasp -> Fmt.string fmt "wasp"
