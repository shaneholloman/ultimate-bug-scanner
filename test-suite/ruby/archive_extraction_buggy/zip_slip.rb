require "fileutils"
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
