package security

import java.net.URI

class ApplicationCall(val request: Request)

class Request(
    val queryParameters: Map<String, String> = emptyMap(),
    val headers: Map<String, String> = emptyMap()
)

class HttpClient {
    fun get(url: String): String = url
    fun post(url: String): String = url
}

class CleanKotlinRequestUrls {
    private val client = HttpClient()
    private val allowedHosts = setOf("api.example.com", "hooks.example.com")

    private fun safeOutboundUrl(raw: String): String {
        val uri = URI.create(raw)
        if (uri.scheme != "https" || uri.host !in allowedHosts) {
            throw IllegalArgumentException("blocked outbound URL")
        }
        return uri.toString()
    }

    fun fetchQueryUrl(call: ApplicationCall): String {
        val target = safeOutboundUrl(call.request.queryParameters["url"] ?: "https://api.example.com")
        return client.get(target)
    }

    fun fetchHeaderUrl(call: ApplicationCall): String {
        val callback = safeOutboundUrl(call.request.headers["X-Callback-Url"] ?: "https://hooks.example.com")
        return client.post(callback)
    }
}
