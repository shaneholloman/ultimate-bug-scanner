package security

import java.net.URLEncoder
import java.nio.charset.StandardCharsets

class ApplicationCall(val request: Request, val response: Response)

class Request(
    val queryParameters: Map<String, String> = emptyMap(),
    val headers: Map<String, String> = emptyMap()
)

class Response(val headers: Headers = Headers()) {
    fun header(name: String, value: String) {}
}

class Headers {
    fun append(name: String, value: String) {}
    operator fun set(name: String, value: String) {}
}

class CleanKotlinHeaders {
    private fun safeHeaderValue(raw: String): String {
        return raw.replace("\r", "").replace("\n", "")
    }

    fun displayName(call: ApplicationCall) {
        val name = safeHeaderValue(call.request.queryParameters["display"] ?: "")
        call.response.header("X-Display-Name", name)
    }

    fun downloadFilename(call: ApplicationCall) {
        val filename = URLEncoder.encode(
            call.request.queryParameters["filename"] ?: "download.txt",
            StandardCharsets.UTF_8
        )
        call.response.headers.append("Content-Disposition", "attachment; filename=\"$filename\"")
    }

    fun traceHeader(call: ApplicationCall) {
        val traceId = call.request.headers["X-Trace-Id"] ?: ""
        require(!traceId.contains('\r') && !traceId.contains('\n')) { "bad header value" }
        call.response.headers["X-Trace-Id"] = traceId
    }
}
