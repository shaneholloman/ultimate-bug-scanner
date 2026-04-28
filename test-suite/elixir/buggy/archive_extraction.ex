defmodule BuggyArchiveExtraction do
  def extract_zip_to_cwd(archive_path, destination) do
    :zip.extract(String.to_charlist(archive_path), cwd: String.to_charlist(destination))
  end

  def extract_tar_to_cwd(archive_path, destination) do
    :erl_tar.extract(String.to_charlist(archive_path), [:compressed, {:cwd, String.to_charlist(destination)}])
  end

  def extract_zip_memory(archive_path, destination) do
    {:ok, files} = :zip.extract(String.to_charlist(archive_path), [:memory])

    Enum.each(files, fn {name, contents} ->
      target = Path.join(destination, List.to_string(name))
      File.write!(target, contents)
    end)
  end

  def extract_tar_memory(archive_path, destination) do
    {:ok, files} = :erl_tar.extract(String.to_charlist(archive_path), [:compressed, :memory])

    Enum.each(files, fn {path, contents} ->
      target = Path.join(destination, List.to_string(path))
      File.write!(target, contents)
    end)
  end
end
