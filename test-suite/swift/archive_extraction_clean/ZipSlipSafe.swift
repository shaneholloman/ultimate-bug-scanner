import Foundation
import ZIPFoundation

func safeArchiveURL(destination: URL, entryPath: String) throws -> URL {
    let root = destination.standardizedFileURL
    let target = destination.appendingPathComponent(entryPath).standardizedFileURL
    guard target.path.hasPrefix(root.path + "/") || target == root else {
        throw CocoaError(.fileReadInvalidFileName)
    }
    return target
}

func unzipSafelyWithHelper(archive: Archive, destination: URL) throws {
    for entry in archive {
        let target = try safeArchiveURL(destination: destination, entryPath: entry.path)
        try FileManager.default.createDirectory(
            at: target.deletingLastPathComponent(),
            withIntermediateDirectories: true
        )
        _ = try archive.extract(entry, to: target)
    }
}

func unzipSafelyInline(archive: Archive, destination: URL) throws {
    let root = destination.standardizedFileURL
    for entry in archive {
        let target = destination.appendingPathComponent(entry.path).standardizedFileURL
        guard target.path.hasPrefix(root.path + "/") || target == root else {
            throw CocoaError(.fileReadInvalidFileName)
        }
        try Data().write(to: target)
    }
}
