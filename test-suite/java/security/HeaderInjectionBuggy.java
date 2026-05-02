package security;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import org.springframework.http.HttpHeaders;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RequestParam;

public final class HeaderInjectionBuggy {
    public void servletHeader(HttpServletRequest request, HttpServletResponse response) {
        String displayName = request.getParameter("display_name");
        response.setHeader("X-Display-Name", displayName);
    }

    public void downloadFilename(HttpServletRequest request, HttpServletResponse response) {
        String filename = request.getParameter("filename");
        response.addHeader("Content-Disposition", "attachment; filename=\"" + filename + "\"");
    }

    public ResponseEntity<Void> springHeader(HttpServletRequest request) {
        String trace = request.getHeader("X-Trace-Id");
        return ResponseEntity.ok().header("X-Upstream-Trace", trace).build();
    }

    public ResponseEntity<Void> annotatedHeader(@RequestHeader("X-Trace-Id") String traceId) {
        HttpHeaders headers = new HttpHeaders();
        headers.add("X-Trace-Id", traceId);
        return ResponseEntity.ok().headers(headers).build();
    }

    public ResponseEntity<Void> annotatedQuery(@RequestParam("tenant") String tenant) {
        return ResponseEntity.ok().header("X-Tenant", tenant).build();
    }
}
