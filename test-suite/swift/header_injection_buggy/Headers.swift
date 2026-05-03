import Foundation

struct Content {
    func get<T>(_ type: T.Type, at key: String) throws -> String {
        return key
    }
}

struct CookieJar {
    subscript(name: String) -> String? { name }
}

struct Headers {
    subscript(name: String) -> String? {
        get { name }
        set {}
    }

    func first(name: String) -> String? {
        return name
    }

    mutating func add(name: String, value: String) {}
    mutating func replaceOrAdd(name: String, value: String) {}
}

struct Request {
    let query: [String: String]
    let parameters: [String: String]
    let headers: Headers
    let cookies: CookieJar
    let url: URL
    let content: Content
}

enum Status {
    case ok
}

struct Response {
    var status: Status
    var headers: [String: String]
}

struct HTTPHeaders {
    init(_ pairs: [(String, String)]) {}
}

func displayName(req: Request) -> Response {
    let name = req.query["displayName"] ?? "guest"
    var response = Response(status: .ok, headers: [:])
    response.headers["X-Display-Name"] = name
    return response
}

func download(req: Request) -> Response {
    let filename = req.parameters["filename"] ?? "report.csv"
    return Response(
        status: .ok,
        headers: ["Content-Disposition": "attachment; filename=\(filename)"]
    )
}

func traceHeader(request: Request) -> Response {
    let trace = request.headers.first(name: "X-Trace-ID") ?? ""
    var headers = Headers()
    headers.add(name: "X-Upstream-Trace", value: trace)
    return Response(status: .ok, headers: [:])
}

func contentHeader(req: Request) throws -> Response {
    let tenant = try req.content.get(String.self, at: "tenantHeader")
    var response = Response(status: .ok, headers: [:])
    response.headers["X-Tenant"] = tenant
    return response
}

func cookiesHeader(req: Request) -> HTTPHeaders {
    let exportName = req.cookies["exportName"] ?? "report"
    return HTTPHeaders([("X-Export-Name", exportName)])
}

func mixedLocationAndDisplayHeader(req: Request) -> Response {
    let name = req.query["displayName"] ?? "guest"
    return Response(
        status: .ok,
        headers: ["Location": "/safe", "X-Display-Name": name]
    )
}

func validationAfterWrite(req: Request) throws -> Response {
    let value = req.headers["X-Customer"] ?? ""
    var response = Response(status: .ok, headers: [:])
    response.headers["X-Customer"] = value
    guard !value.contains("\n") else {
        throw NSError(domain: "headers", code: 1)
    }
    return response
}
