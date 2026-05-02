import Foundation

struct Content {
    func get<T>(_ type: T.Type, at key: String) throws -> String { key }
}

struct Headers {
    subscript(name: String) -> String? { name }
    func first(name: String) -> String? { name }
}

struct Request {
    let query: [String: String]
    let parameters: [String: String]
    let headers: Headers
    let url: URL
    let content: Content

    func redirect(to target: String) -> Response {
        Response(status: .found, headers: ["Location": target])
    }
}

enum Status {
    case found
}

struct Response {
    var status: Status
    var headers: [String: String]

    static func redirect(to target: String) -> Response {
        Response(status: .found, headers: ["Location": target])
    }
}

func redirect(to target: String) -> Response {
    Response.redirect(to: target)
}

func queryRedirect(req: Request) -> Response {
    let target = req.query["returnUrl"] ?? "/"
    return req.redirect(to: target)
}

func headerRedirect(request: Request) -> Response {
    let target = request.headers.first(name: "X-Redirect") ?? "/"
    return Response.redirect(to: target)
}

func contentRedirect(req: Request) throws -> Response {
    let redirectURL = try req.content.get(String.self, at: "redirectUrl")
    return redirect(to: redirectURL)
}

func requestUrlRedirect(request: Request) -> Response {
    let target = request.url.absoluteString
    return request.redirect(to: target)
}

func locationHeaderRedirect(req: Request) -> Response {
    let next = req.parameters["next"] ?? "/"
    var response = Response(status: .found, headers: [:])
    response.headers["Location"] = next
    return response
}

func validatesAfterRedirect(req: Request) throws -> Response {
    let target = req.query["continue"] ?? "/"
    let response = req.redirect(to: target)
    guard target.hasPrefix("/") && !target.hasPrefix("//") else {
        throw NSError(domain: "redirect", code: 1)
    }
    return response
}
