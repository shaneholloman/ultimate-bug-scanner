package security;

import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import org.springframework.http.HttpHeaders;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RequestParam;

public final class HeaderInjectionClean {
    private static String safeHeaderValue(String raw) {
        return raw.replace("\r", "").replace("\n", "");
    }

    private static String encodedFilename(String raw) {
        return URLEncoder.encode(raw, StandardCharsets.UTF_8);
    }

    public void servletHeader(HttpServletRequest request, HttpServletResponse response) {
        String displayName = safeHeaderValue(request.getParameter("display_name"));
        response.setHeader("X-Display-Name", displayName);
    }

    public void downloadFilename(HttpServletRequest request, HttpServletResponse response) {
        String filename = encodedFilename(request.getParameter("filename"));
        response.addHeader("Content-Disposition", "attachment; filename=\"" + filename + "\"");
    }

    public void multilineServletHeader(HttpServletRequest request, HttpServletResponse response) {
        String segment = safeHeaderValue(request.getParameter("segment"));
        response.setHeader(
                "X-Segment",
                segment);
    }

    public ResponseEntity<Void> springHeader(HttpServletRequest request) {
        String trace = request.getHeader("X-Trace-Id");
        if (trace.indexOf('\r') >= 0 || trace.indexOf('\n') >= 0) {
            throw new IllegalArgumentException("bad header value");
        }
        return ResponseEntity.ok().header("X-Upstream-Trace", trace).build();
    }

    public ResponseEntity<Void> annotatedHeader(@RequestHeader("X-Trace-Id") String traceId) {
        HttpHeaders headers = new HttpHeaders();
        headers.add("X-Trace-Id", safeHeaderValue(traceId));
        return ResponseEntity.ok().headers(headers).build();
    }

    public ResponseEntity<Void> annotatedQuery(@RequestParam("tenant") String tenant) {
        return ResponseEntity.ok().header("X-Tenant", safeHeaderValue(tenant)).build();
    }
}
