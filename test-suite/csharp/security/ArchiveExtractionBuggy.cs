using System.IO;
using System.IO.Compression;
using System.Formats.Tar;
using ICSharpCode.SharpZipLib.Zip;
using SharpCompress.Archives;

public static class ArchiveExtractionBuggy
{
    public static void UnzipWithPathCombine(ZipArchive archive, string destination)
    {
        foreach (var entry in archive.Entries)
        {
            var target = Path.Combine(destination, entry.FullName);
            Directory.CreateDirectory(Path.GetDirectoryName(target)!);
            entry.ExtractToFile(target, overwrite: true);
        }
    }

    public static void UnzipWithEntryNameAlias(ZipInputStream zipStream, string destination)
    {
        ZipEntry? entry;
        while ((entry = zipStream.GetNextEntry()) != null)
        {
            var name = entry.Name;
            var target = destination + Path.DirectorySeparatorChar + name;
            using var output = File.Create(target);
            zipStream.CopyTo(output);
        }
    }

    public static void UntarWithInterpolation(TarReader reader, string destination)
    {
        TarEntry? entry;
        while ((entry = reader.GetNextEntry()) != null)
        {
            var target = $"{destination}/{entry.Name}";
            using var output = File.OpenWrite(target);
            entry.DataStream?.CopyTo(output);
        }
    }

    public static void ExtractSharpCompressEntry(IArchiveEntry entry, string destination)
    {
        var target = Path.Join(destination, entry.Key);
        entry.WriteToFile(target);
    }
}
