package security;

import java.io.IOException;
import java.net.URI;
import java.net.URL;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.util.Set;
import javax.servlet.http.HttpServletRequest;
import org.springframework.web.client.RestTemplate;

public final class SsrfClean {
    private static final Set<String> ALLOWED_HOSTS = Set.of(
            "api.example.com",
            "hooks.example.com");

    private final HttpClient httpClient = HttpClient.newHttpClient();
    private final RestTemplate restTemplate = new RestTemplate();

    private static String safeOutboundUrl(String raw) {
        URI parsed = URI.create(raw);
        if (!"https".equals(parsed.getScheme()) || !ALLOWED_HOSTS.contains(parsed.getHost())) {
            throw new IllegalArgumentException("blocked outbound URL");
        }
        return parsed.toString();
    }

    private static URI safeOutboundUri(String raw) {
        return URI.create(safeOutboundUrl(raw));
    }

    public HttpResponse<String> fetchFromQuery(HttpServletRequest request)
            throws IOException, InterruptedException {
        String target = safeOutboundUrl(request.getParameter("url"));
        HttpRequest outbound = HttpRequest.newBuilder(URI.create(target)).GET().build();
        return httpClient.send(outbound, HttpResponse.BodyHandlers.ofString());
    }

    public Object fetchCallback(HttpServletRequest request) {
        String callback = safeOutboundUrl(request.getHeader("X-Callback-Url"));
        return restTemplate.getForObject(callback, String.class);
    }

    public Object openStream(HttpServletRequest request) throws IOException {
        String next = safeOutboundUrl(request.getParameter("next"));
        return new URL(next).openStream();
    }

    public HttpResponse<String> fetchByHost(HttpServletRequest request)
            throws IOException, InterruptedException {
        URI target = safeOutboundUri(request.getParameter("hostUrl"));
        return httpClient.send(HttpRequest.newBuilder(target).GET().build(),
                HttpResponse.BodyHandlers.ofString());
    }

    public HttpResponse<String> fetchAllowedInboundHost(HttpServletRequest request)
            throws IOException, InterruptedException {
        URI target = safeOutboundUri("https://" + request.getServerName() + "/status");
        return httpClient.send(HttpRequest.newBuilder(target).GET().build(),
                HttpResponse.BodyHandlers.ofString());
    }
}
