defmodule CleanArchiveExtraction do
  def safe_archive_path(destination, entry_name) do
    root = Path.expand(destination)
    target = Path.expand(Path.join(root, entry_name))

    unless target == root or String.starts_with?(target, root <> "/") do
      raise ArgumentError, "archive entry escapes destination"
    end

    target
  end

  def extract_zip_memory(archive_path, destination) do
    {:ok, files} = :zip.extract(String.to_charlist(archive_path), [:memory])

    Enum.each(files, fn {name, contents} ->
      target = safe_archive_path(destination, List.to_string(name))
      File.write!(target, contents)
    end)
  end

  def extract_tar_memory(archive_path, destination) do
    {:ok, files} = :erl_tar.extract(String.to_charlist(archive_path), [:compressed, :memory])

    Enum.each(files, fn {path, contents} ->
      target = safe_archive_path(destination, List.to_string(path))
      File.write!(target, contents)
    end)
  end
end
