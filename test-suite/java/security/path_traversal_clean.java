package security;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

final class PathTraversalClean {
    interface Request {
        String getParameter(String name);
        Part getPart(String name);
    }

    interface Part {
        String getSubmittedFileName();
    }

    Path safeUnderRoot(Path root, String raw) throws IOException {
        Path base = root.toRealPath().normalize();
        Path target = base.resolve(raw).normalize();
        if (!target.startsWith(base)) {
            throw new IOException("path escapes root");
        }
        return target;
    }

    byte[] downloadCheckedFile(Request request, Path documentRoot) throws IOException {
        Path target = safeUnderRoot(documentRoot, request.getParameter("file"));
        return Files.readAllBytes(target);
    }

    void saveCheckedUpload(Request request, Path uploadRoot) throws IOException {
        Part avatar = request.getPart("avatar");
        Path fileName = Paths.get(avatar.getSubmittedFileName()).getFileName();
        Files.write(uploadRoot.resolve(fileName), "avatar".getBytes(StandardCharsets.UTF_8));
    }
}
