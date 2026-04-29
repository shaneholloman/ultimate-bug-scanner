import java.io.File
import java.nio.file.Files
import java.nio.file.Path
import java.util.zip.ZipFile
import java.util.zip.ZipInputStream

fun unzipWithZipFile(archive: File, destination: Path) {
    ZipFile(archive).use { zip ->
        zip.entries().asSequence().forEach { entry ->
            val target = destination.resolve(entry.name)
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

fun unzipWithAlias(stream: ZipInputStream, destination: File) {
    generateSequence { stream.nextEntry }.forEach { entry ->
        val name = entry.name
        val target = File(destination, name)
        Files.copy(stream, target.toPath())
    }
}

fun unzipDirect(stream: ZipInputStream, destination: Path) {
    var entry = stream.nextEntry
    while (entry != null) {
        Files.write(destination.resolve(entry.name), stream.readBytes())
        entry = stream.nextEntry
    }
}
