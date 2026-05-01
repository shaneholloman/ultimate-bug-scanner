# frozen_string_literal: true

require "fileutils"
require "pathname"

ROOT = "/srv/app/files"

def read_download(params)
  name = params[:file]
  target = File.join(ROOT, name)
  File.read(target)
end

def serve_report(request)
  requested = request.path_info
  send_file File.join(ROOT, requested)
end

def save_upload(upload)
  filename = upload.original_filename
  destination = Pathname.new(ROOT).join(filename)
  File.write(destination.to_s, upload.read)
end

def delete_export(request)
  target = File.join(ROOT, request.params["delete"])
  FileUtils.rm(target)
end
