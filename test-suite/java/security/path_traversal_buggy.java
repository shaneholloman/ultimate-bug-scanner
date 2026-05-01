package security;

import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

final class PathTraversalBuggy {
    interface Request {
        String getParameter(String name);
        String getPathInfo();
        Part getPart(String name);
    }

    interface Part {
        String getSubmittedFileName();
    }

    byte[] downloadQueryFile(Request request, Path documentRoot) throws IOException {
        String name = request.getParameter("file");
        return Files.readAllBytes(documentRoot.resolve(name));
    }

    void streamRawRequestPath(Request request, File documentRoot) throws IOException {
        String rawPath = request.getPathInfo();
        try (FileInputStream input = new FileInputStream(new File(documentRoot, rawPath))) {
            input.read();
        }
    }

    void saveSubmittedFile(Request request, Path uploadRoot) throws IOException {
        Part avatar = request.getPart("avatar");
        Path target = uploadRoot.resolve(avatar.getSubmittedFileName());
        Files.writeString(target, "avatar");
    }

    void deleteFormSelection(Request request, Path uploadRoot) throws IOException {
        Path target = uploadRoot.resolve(request.getParameter("delete"));
        Files.deleteIfExists(target);
    }

}
