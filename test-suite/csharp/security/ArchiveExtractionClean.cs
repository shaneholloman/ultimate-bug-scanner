using System;
using System.IO;
using System.IO.Compression;
using System.Formats.Tar;
using SharpCompress.Archives;

public static class ArchiveExtractionClean
{
    private static string GetSafeExtractionPath(string destination, string entryName)
    {
        var destinationRoot = Path.GetFullPath(destination);
        var target = Path.GetFullPath(Path.Combine(destinationRoot, entryName));
        if (!target.StartsWith(destinationRoot + Path.DirectorySeparatorChar, StringComparison.Ordinal) &&
            !string.Equals(target, destinationRoot, StringComparison.Ordinal))
        {
            throw new InvalidOperationException("Archive entry escapes destination");
        }

        return target;
    }

    public static void UnzipSafely(ZipArchive archive, string destination)
    {
        foreach (var entry in archive.Entries)
        {
            var target = GetSafeExtractionPath(destination, entry.FullName);
            Directory.CreateDirectory(Path.GetDirectoryName(target)!);
            entry.ExtractToFile(target, overwrite: true);
        }
    }

    public static void UntarSafely(TarReader reader, string destination)
    {
        while (reader.GetNextEntry() is { } entry)
        {
            var target = Path.GetFullPath(Path.Combine(destination, entry.Name));
            var root = Path.GetFullPath(destination);
            if (!target.StartsWith(root + Path.DirectorySeparatorChar, StringComparison.Ordinal))
            {
                throw new InvalidOperationException("Archive entry escapes destination");
            }

            using var output = File.OpenWrite(target);
            entry.DataStream?.CopyTo(output);
        }
    }

    public static void ExtractSharpCompressEntry(IArchiveEntry entry, string destination)
    {
        var target = GetSafeExtractionPath(destination, entry.Key);
        entry.WriteToFile(target);
    }
}
