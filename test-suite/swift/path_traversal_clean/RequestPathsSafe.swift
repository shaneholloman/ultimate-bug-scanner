import Foundation

struct UploadedFile {
    let filename: String
    let data: Data
}

struct FileIO {
    func streamFile(at path: String) -> String {
        return path
    }
}

struct Request {
    let query: [String: String]
    let headers: [String: String]
    let url: URL
    let file: UploadedFile
    let fileio: FileIO
}

enum PathError: Error {
    case escapedRoot
}

let documentRoot = URL(fileURLWithPath: "/srv/app/files")

func safeUnderRoot(_ base: URL, _ requested: String) throws -> URL {
    let root = base.standardizedFileURL
    let candidate = root.appendingPathComponent(requested).standardizedFileURL
    guard candidate.path == root.path || candidate.path.hasPrefix(root.path + "/") else {
        throw PathError.escapedRoot
    }
    return candidate
}

func readDownload(req: Request) throws -> String {
    let requestedName = req.query["file"] ?? "index.html"
    let target = try safeUnderRoot(documentRoot, requestedName)
    return try String(contentsOf: target)
}

func serveRawURLPath(request: Request) throws -> String {
    let target = try safeUnderRoot(documentRoot, request.url.path)
    return request.fileio.streamFile(at: target.path)
}

func saveUpload(req: Request) throws {
    let safeName = URL(fileURLWithPath: req.file.filename).lastPathComponent
    let destination = documentRoot.appendingPathComponent(safeName)
    try req.file.data.write(to: destination)
}

func deleteRequestedExport(req: Request) throws {
    let requested = req.query["delete"] ?? ""
    let target = try safeUnderRoot(documentRoot, requested)
    try FileManager.default.removeItem(at: target)
}

func readHeaderSelectedFile(request: Request) throws -> String {
    let requested = request.headers["X-File-Path"] ?? "index.html"
    let target = try safeUnderRoot(documentRoot, requested)
    return try String(contentsOfFile: target.path)
}

func deleteHeaderSelectedFile(request: Request) throws {
    let requested = request.headers["X-Delete-Path"] ?? ""
    let target = try safeUnderRoot(documentRoot, requested)
    try FileManager.default.removeItem(at: target)
}
