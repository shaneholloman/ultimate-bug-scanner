# frozen_string_literal: true

require "fileutils"

ROOT = "/srv/app/files"

def safe_under_root(root, requested)
  base = File.expand_path(root)
  target = File.expand_path(requested.to_s, base)
  unless target.start_with?(base + File::SEPARATOR) || target == base
    raise ArgumentError, "path escapes root"
  end
  target
end

def read_download(params)
  target = safe_under_root(ROOT, params[:file])
  File.read(target)
end

def save_upload(upload)
  filename = File.basename(upload.original_filename.to_s)
  destination = File.join(ROOT, filename)
  File.write(destination, upload.read)
end

def delete_export(request)
  target = safe_under_root(ROOT, request.params["delete"])
  FileUtils.rm(target)
end

def read_header_file(request)
  target = safe_under_root(ROOT, request.headers["X-File-Path"])
  File.read(target)
end

def serve_env_header(env)
  target = safe_under_root(ROOT, env["HTTP_X_REPORT_PATH"])
  send_file target
end
