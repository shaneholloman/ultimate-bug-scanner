import java.io.File
import java.nio.file.Files
import java.nio.file.Path

class ApplicationCall(
    val parameters: Map<String, String>,
    val request: Request
) {
    fun respondFile(file: File) {}
}

class Request(private val rawPath: String) {
    fun path(): String = rawPath
}

class UploadedPart(
    val originalFileName: String?,
    val source: Path
)

class BuggyKotlinRequestPaths {
    fun download(call: ApplicationCall, root: Path): String {
        val requested = call.parameters["file"] ?: "index.html"
        val target = root.resolve(requested)
        return Files.readString(target)
    }

    fun serveRawPath(call: ApplicationCall, root: File) {
        val rawPath = call.request.path()
        call.respondFile(File(root, rawPath))
    }

    fun saveUpload(part: UploadedPart, uploadRoot: Path) {
        val original = part.originalFileName ?: "upload.bin"
        val target = uploadRoot.resolve(original)
        Files.copy(part.source, target)
    }

    fun deleteExport(call: ApplicationCall, exportRoot: Path) {
        val target = exportRoot.resolve(call.parameters["delete"] ?: "")
        Files.deleteIfExists(target)
    }
}
