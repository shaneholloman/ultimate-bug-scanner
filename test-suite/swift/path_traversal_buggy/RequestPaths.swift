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

let documentRoot = "/srv/app/files"

func readDownload(req: Request) throws -> String {
    let requestedName = req.query["file"] ?? "index.html"
    let path = documentRoot + "/" + requestedName
    return try String(contentsOfFile: path)
}

func serveRawURLPath(request: Request) -> String {
    let requestedPath = request.url.path
    return request.fileio.streamFile(at: documentRoot + requestedPath)
}

func saveUpload(req: Request) throws {
    let destination = URL(fileURLWithPath: documentRoot).appendingPathComponent(req.file.filename)
    try req.file.data.write(to: destination)
}

func deleteRequestedExport(req: Request) throws {
    let target = URL(fileURLWithPath: documentRoot).appendingPathComponent(req.query["delete"] ?? "")
    try FileManager.default.removeItem(at: target)
}

func readHeaderSelectedFile(request: Request) throws -> String {
    let requested = request.headers["X-File-Path"] ?? "index.html"
    let target = URL(fileURLWithPath: documentRoot).appendingPathComponent(requested)
    return try String(contentsOfFile: target.path)
}

func deleteHeaderSelectedFile(request: Request) throws {
    let target = URL(fileURLWithPath: documentRoot).appendingPathComponent(request.headers["X-Delete-Path"] ?? "")
    try FileManager.default.removeItem(at: target)
}
