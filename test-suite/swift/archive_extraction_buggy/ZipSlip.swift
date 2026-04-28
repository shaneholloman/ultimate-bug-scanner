import Foundation
import ZIPFoundation

func unzipWithAppendingPathComponent(archive: Archive, destination: URL) throws {
    for entry in archive {
        let target = destination.appendingPathComponent(entry.path)
        try FileManager.default.createDirectory(
            at: target.deletingLastPathComponent(),
            withIntermediateDirectories: true
        )
        _ = try archive.extract(entry, to: target)
    }
}

func unzipWithAliasedEntryPath(archive: Archive, destination: URL) throws {
    for entry in archive {
        let name = entry.path
        let target = destination.appendingPathComponent(name)
        let data = Data()
        try data.write(to: target)
    }
}

func unzipWithStringPath(archive: Archive, destinationPath: String) throws {
    for entry in archive {
        let target = "\(destinationPath)/\(entry.path)"
        FileManager.default.createFile(atPath: target, contents: Data())
    }
}
