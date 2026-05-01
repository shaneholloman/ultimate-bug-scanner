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

func fetchQueryURL(req: Request) {
    let target = req.query["url"] ?? "https://example.com"
    URLSession.shared.dataTask(with: URL(string: target)!).resume()
}

func fetchCallbackHeader(request: Request) async throws -> (Data, URLResponse) {
    let callback = request.headers["X-Callback-Url"] ?? "https://example.com/callback"
    return try await URLSession.shared.data(from: URL(string: callback)!)
}

func fetchViaURLRequest(req: Request, session: URLSession) async throws -> (Data, URLResponse) {
    let endpoint = req.parameters["endpoint"] ?? "https://example.com/api"
    let outboundRequest = URLRequest(url: URL(string: endpoint)!)
    return try await session.data(for: outboundRequest)
}

func loadWebhookBody(req: Request) throws -> Data {
    let webhook = try req.content.get(String.self, at: "webhookUrl")
    return try Data(contentsOf: URL(string: webhook)!)
}

func fetchHost(req: Request, client: HTTPClient) async throws -> Data {
    let host = req.query["host"] ?? "metadata.internal"
    return try await client.get(url: "https://\(host)/internal/status")
}

func validateTooLate(req: Request) {
    let target = req.query["lateUrl"] ?? "https://example.com"
    URLSession.shared.dataTask(with: URL(string: target)!).resume()
    guard URL(string: target)?.host == "api.example.com" else {
        return
    }
}
