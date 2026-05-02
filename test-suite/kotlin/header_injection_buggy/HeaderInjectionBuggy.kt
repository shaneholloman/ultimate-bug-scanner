package security

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

class BuggyKotlinHeaders {
    fun displayName(call: ApplicationCall) {
        val name = call.request.queryParameters["display"] ?: ""
        call.response.header("X-Display-Name", name)
    }

    fun downloadFilename(call: ApplicationCall) {
        val filename = call.request.queryParameters["filename"] ?: "download.txt"
        call.response.headers.append("Content-Disposition", "attachment; filename=\"$filename\"")
    }

    fun traceHeader(call: ApplicationCall) {
        val traceId = call.request.headers["X-Trace-Id"] ?: ""
        call.response.headers["X-Trace-Id"] = traceId
    }
}
