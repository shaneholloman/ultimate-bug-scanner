package security;

import java.io.IOException;
import java.io.OutputStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.zip.ZipEntry;
import java.util.zip.ZipInputStream;

final class ArchiveExtractionClean {
    void unzipSafely(Path destination, ZipInputStream archive) throws IOException {
        Path base = destination.toRealPath().normalize();
        ZipEntry entry;
        while ((entry = archive.getNextEntry()) != null) {
            Path target = safeDestination(base, entry.getName());
            if (entry.isDirectory()) {
                Files.createDirectories(target);
                continue;
            }
            Files.createDirectories(target.getParent());
            try (OutputStream output = Files.newOutputStream(target)) {
                archive.transferTo(output);
            }
        }
    }

    void unzipWithInlineCheck(Path destination, ZipInputStream archive) throws IOException {
        Path base = destination.toRealPath().normalize();
        ZipEntry entry;
        while ((entry = archive.getNextEntry()) != null) {
            Path target = base.resolve(entry.getName()).normalize();
            if (!target.startsWith(base)) {
                throw new IOException("archive entry escapes destination");
            }
            if (entry.isDirectory()) {
                Files.createDirectories(target);
                continue;
            }
            Files.copy(archive, target);
        }
    }

    private Path safeDestination(Path base, String entryName) throws IOException {
        Path target = base.resolve(entryName).normalize();
        if (!target.startsWith(base)) {
            throw new IOException("archive entry escapes destination");
        }
        return target;
    }
}
