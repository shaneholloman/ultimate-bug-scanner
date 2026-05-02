package security

class ApplicationCall(val request: Request)

class Request(
    val queryParameters: Map<String, String> = emptyMap(),
    val headers: Map<String, String> = emptyMap()
)

class HttpClient {
    fun get(url: String): String = url
    fun post(url: String): String = url
}

class BuggyKotlinRequestUrls {
    private val client = HttpClient()

    fun fetchQueryUrl(call: ApplicationCall): String {
        val target = call.request.queryParameters["url"] ?: "https://example.com"
        return client.get(target)
    }

    fun fetchHeaderUrl(call: ApplicationCall): String {
        val callback = call.request.headers["X-Callback-Url"] ?: "https://example.com"
        return client.post(callback)
    }
}
