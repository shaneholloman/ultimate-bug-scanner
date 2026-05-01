import Foundation

struct Content {
    func get<T>(_ type: T.Type, at key: String) throws -> String {
        return key
    }
}

struct Request {
    let query: [String: String]
    let parameters: [String: String]
    let headers: [String: String]
    let url: URL
    let content: Content
}

struct HTTPClient {
    func get(url: String) async throws -> Data {
        return Data(url.utf8)
    }
}

enum URLSafetyError: Error {
    case blocked
}

let allowedHosts = Set(["api.example.com", "hooks.example.com"])

func safeOutboundURL(_ raw: String) throws -> URL {
    guard
        let url = URL(string: raw),
        url.scheme == "https",
        let host = url.host,
        allowedHosts.contains(host)
    else {
        throw URLSafetyError.blocked
    }
    return url
}

func fetchQueryURL(req: Request) throws {
    let target = try safeOutboundURL(req.query["url"] ?? "https://api.example.com")
    URLSession.shared.dataTask(with: target).resume()
}

func fetchCallbackHeader(request: Request) async throws -> (Data, URLResponse) {
    let callback = try safeOutboundURL(request.headers["X-Callback-Url"] ?? "https://hooks.example.com/callback")
    return try await URLSession.shared.data(from: callback)
}

func fetchViaURLRequest(req: Request, session: URLSession) async throws -> (Data, URLResponse) {
    let endpoint = try safeOutboundURL(req.parameters["endpoint"] ?? "https://api.example.com/api")
    let outboundRequest = URLRequest(url: endpoint)
    return try await session.data(for: outboundRequest)
}

func loadWebhookBody(req: Request) throws -> Data {
    let webhook = try safeOutboundURL(try req.content.get(String.self, at: "webhookUrl"))
    return try Data(contentsOf: webhook)
}

func fetchHost(req: Request, client: HTTPClient) async throws -> Data {
    let target = try safeOutboundURL(req.query["url"] ?? "https://api.example.com/internal/status")
    return try await client.get(url: target.absoluteString)
}

func fetchAfterInlineValidation(req: Request) {
    let raw = req.query["next"] ?? "https://api.example.com/next"
    guard
        let url = URL(string: raw),
        url.scheme == "https",
        let host = url.host,
        allowedHosts.contains(host)
    else {
        return
    }
    URLSession.shared.dataTask(with: url).resume()
}
