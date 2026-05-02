package security

class ApplicationCall(val request: Request) {
    fun respondRedirect(location: String) {}
}

class Request(
    val queryParameters: Map<String, String> = emptyMap(),
    val headers: Map<String, String> = emptyMap()
)

class BuggyKotlinRedirects {
    fun redirectQuery(call: ApplicationCall) {
        val target = call.request.queryParameters["next"] ?: "/"
        call.respondRedirect(target)
    }

    fun redirectHeader(call: ApplicationCall): String {
        val target = call.request.headers["X-Return-To"] ?: "/"
        return "redirect:$target"
    }
}
