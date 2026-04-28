require "fileutils"
require "pathname"
require "zip"
require "rubygems/package"

def safe_archive_path(destination, entry_name)
  base = File.expand_path(destination)
  target = File.expand_path(entry_name, base)
  unless target.start_with?(base + File::SEPARATOR) || target == base
    raise ArgumentError, "archive entry escapes destination"
  end
  target
end

def unzip_safely(archive_path, destination)
  Zip::File.open(archive_path) do |zip_file|
    zip_file.each do |entry|
      target = safe_archive_path(destination, entry.name)
      FileUtils.mkdir_p(File.dirname(target))
      entry.extract(target) { true }
    end
  end
end

def untar_safely(io, destination)
  base = File.expand_path(destination)
  Gem::Package::TarReader.new(io).each do |entry|
    target = File.expand_path(entry.full_name, base)
    unless target.start_with?(base + File::SEPARATOR) || target == base
      raise ArgumentError, "archive entry escapes destination"
    end
    FileUtils.mkdir_p(File.dirname(target))
    File.binwrite(target, entry.read)
  end
end

def untar_with_pathname_safely(io, destination)
  base = Pathname.new(destination).realpath
  Minitar::Reader.open(io).each do |entry|
    target = (Pathname.new(base.to_s) + entry.full_name).cleanpath
    unless target.to_s.start_with?(base.to_s + File::SEPARATOR) || target == base
      raise ArgumentError, "archive entry escapes destination"
    end
    FileUtils.mkdir_p(target.dirname)
    File.binwrite(target.to_s, entry.read)
  end
end

def unzip_with_safe_interpolation(archive_path, destination)
  Zip::InputStream.open(archive_path) do |zip_stream|
    while (entry = zip_stream.get_next_entry)
      target = safe_archive_path(destination, entry.path)
      FileUtils.mkdir_p(File.dirname(target))
      File.binwrite(target, zip_stream.read)
    end
  end
end
