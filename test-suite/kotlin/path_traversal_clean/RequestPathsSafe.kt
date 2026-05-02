import java.io.File
import java.nio.file.Files
import java.nio.file.Path
import kotlin.io.path.name

class ApplicationCall(
    val parameters: Map<String, String>,
    val request: Request
) {
    fun respondFile(file: File) {}
}

class Request(
    private val rawPath: String,
    val headers: Map<String, String> = emptyMap()
) {
    fun path(): String = rawPath
}

class UploadedPart(
    val originalFileName: String?,
    val source: Path
)

class CleanKotlinRequestPaths {
    private fun safeUnderRoot(root: Path, raw: String): Path {
        val base = root.toRealPath().normalize()
        val target = base.resolve(raw).normalize()
        if (!target.startsWith(base)) {
            throw IllegalArgumentException("path escapes root")
        }
        return target
    }

    fun download(call: ApplicationCall, root: Path): String {
        val requested = call.parameters["file"] ?: "index.html"
        val target = safeUnderRoot(root, requested)
        return Files.readString(target)
    }

    fun serveRawPath(call: ApplicationCall, root: Path) {
        val target = safeUnderRoot(root, call.request.path())
        call.respondFile(target.toFile())
    }

    fun saveUpload(part: UploadedPart, uploadRoot: Path) {
        val safeName = Path.of(part.originalFileName ?: "upload.bin").fileName.toString()
        val target = uploadRoot.resolve(safeName)
        Files.copy(part.source, target)
    }

    fun deleteExport(call: ApplicationCall, exportRoot: Path) {
        val requested = call.parameters["delete"] ?: ""
        val target = safeUnderRoot(exportRoot, requested)
        Files.deleteIfExists(target)
    }

    fun readHeaderFile(call: ApplicationCall, root: Path): String {
        val requested = call.request.headers["X-File-Path"] ?: "index.html"
        val target = safeUnderRoot(root, requested)
        return Files.readString(target)
    }
}
