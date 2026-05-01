defmodule CleanRequestPathTraversal do
  import Plug.Conn

  def safe_under_root(root, requested) do
    base = Path.expand(root)
    target = Path.expand(Path.join(base, requested))

    unless target == base or String.starts_with?(target, base <> "/") do
      raise ArgumentError, "path escapes root"
    end

    target
  end

  def read_download(conn) do
    requested = conn.params["file"] || "index.txt"
    path = safe_under_root("/srv/app/files", requested)
    File.read!(path)
  end

  def send_asset(conn) do
    path = safe_under_root("/srv/app/files", conn.request_path)
    send_file(conn, 200, path)
  end

  def save_upload(_conn, upload) do
    name = Path.basename(upload.filename)
    target = Path.join("/srv/app/uploads", name)
    File.cp!(upload.path, target)
  end

  def delete_export(conn) do
    requested = conn.params["delete"] || ""
    target = safe_under_root("/srv/app/exports", requested)
    File.rm!(target)
  end
end
