defmodule BuggyRequestPathTraversal do
  import Plug.Conn

  def read_download(conn) do
    name = conn.params["file"]
    path = "/srv/app/files/" <> name
    File.read!(path)
  end

  def send_asset(conn) do
    requested_path = conn.request_path
    send_file(conn, 200, "/srv/app/files" <> requested_path)
  end

  def save_upload(_conn, upload) do
    target = Path.join("/srv/app/uploads", upload.filename)
    File.cp!(upload.path, target)
  end

  def delete_export(conn) do
    target = Path.join("/srv/app/exports", conn.params["delete"])
    File.rm!(target)
  end

  def read_header_file(conn) do
    requested = Plug.Conn.get_req_header(conn, "x-file-path") |> List.first()
    target = Path.join("/srv/app/files", requested)
    File.read!(target)
  end
end
