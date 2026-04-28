package security;

import java.io.File;
import java.io.IOException;
import java.io.OutputStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.zip.ZipEntry;
import java.util.zip.ZipInputStream;

final class ArchiveExtractionBuggy {
    void unzipWithResolve(Path destination, ZipInputStream archive) throws IOException {
        ZipEntry entry;
        while ((entry = archive.getNextEntry()) != null) {
            Path target = destination.resolve(entry.getName());
            if (entry.isDirectory()) {
                Files.createDirectories(target);
                continue;
            }
            Files.createDirectories(target.getParent());
            Files.copy(archive, target);
        }
    }

    void unzipWithFile(File destination, ZipInputStream archive) throws IOException {
        ZipEntry entry;
        while ((entry = archive.getNextEntry()) != null) {
            String name = entry.getName();
            File target = new File(destination, name);
            if (entry.isDirectory()) {
                target.mkdirs();
                continue;
            }
            try (OutputStream output = Files.newOutputStream(target.toPath())) {
                archive.transferTo(output);
            }
        }
    }
}
