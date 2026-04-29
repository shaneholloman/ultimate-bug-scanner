import java.io.File
import java.nio.file.Files
import java.nio.file.Path
import java.util.zip.ZipFile
import java.util.zip.ZipInputStream

private fun safeArchivePath(destination: Path, entryName: String): Path {
    val base = destination.toAbsolutePath().normalize()
    val target = base.resolve(entryName).normalize()
    require(target.startsWith(base)) { "archive entry escapes destination" }
    return target
}

fun unzipWithZipFileSafely(archive: File, destination: Path) {
    ZipFile(archive).use { zip ->
        zip.entries().asSequence().forEach { entry ->
            val target = safeArchivePath(destination, entry.name)
            if (entry.isDirectory) {
                Files.createDirectories(target)
            } else {
                Files.createDirectories(target.parent)
                zip.getInputStream(entry).use { input ->
                    Files.copy(input, target)
                }
            }
        }
    }
}

fun unzipInlineSafely(stream: ZipInputStream, destination: File) {
    val base = destination.toPath().toAbsolutePath().normalize()
    generateSequence { stream.nextEntry }.forEach { entry ->
        val target = base.resolve(entry.name).normalize()
        require(target.startsWith(base)) { "archive entry escapes destination" }
        Files.copy(stream, target)
    }
}
