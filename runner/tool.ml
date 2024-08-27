open Bos

type tool_type =
  | Owi
  | Wasp

type t =
  { tool : tool_type
  ; flags : string list
  }

let make ?(flags = []) tool = { tool; flags }

let cmd { tool; flags } workspace file =
  match tool with
  | Owi ->
      Cmd.(
        v "owi" % "sym" %% of_list flags % "--workspace" % p workspace % p file)
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
