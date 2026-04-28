require "fileutils"
require "pathname"
require "zip"
require "rubygems/package"

def unzip_unsafe(archive_path, destination)
  Zip::File.open(archive_path) do |zip_file|
    zip_file.each do |entry|
      target = File.join(destination, entry.name)
      FileUtils.mkdir_p(File.dirname(target))
      entry.extract(target) { true }
    end
  end
end

def untar_unsafe(io, destination)
  Gem::Package::TarReader.new(io).each do |entry|
    name = entry.full_name
    target = File.join(destination, name)
    FileUtils.mkdir_p(File.dirname(target))
    File.binwrite(target, entry.read)
  end
end

def unzip_with_pathname_unsafe(archive_path, destination)
  Zip::InputStream.open(archive_path) do |zip_stream|
    while (entry = zip_stream.get_next_entry)
      target = Pathname.new(destination) + entry.path
      FileUtils.mkdir_p(target.dirname)
      File.binwrite(target.to_s, zip_stream.read)
    end
  end
end

def untar_with_string_concat_unsafe(io, destination)
  Minitar::Reader.open(io).each do |entry|
    target = destination + "/" + entry.full_name
    FileUtils.mkdir_p(File.dirname(target))
    File.binwrite(target, entry.read)
  end
end

def untar_with_interpolation_unsafe(io, destination)
  Archive::Reader.open(io).each do |entry|
    name = entry.path
    target = "#{destination}/#{name}"
    FileUtils.mkdir_p(File.dirname(target))
    File.binwrite(target, entry.read)
  end
end
