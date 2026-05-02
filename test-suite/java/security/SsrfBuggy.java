package security;

import java.io.IOException;
import java.net.URI;
import java.net.URL;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import javax.servlet.http.HttpServletRequest;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.client.RestTemplate;

public final class SsrfBuggy {
    private final HttpClient httpClient = HttpClient.newHttpClient();
    private final RestTemplate restTemplate = new RestTemplate();

    public HttpResponse<String> fetchFromQuery(HttpServletRequest request)
            throws IOException, InterruptedException {
        String target = request.getParameter("url");
        HttpRequest outbound = HttpRequest.newBuilder(URI.create(target)).GET().build();
        return httpClient.send(outbound, HttpResponse.BodyHandlers.ofString());
    }

    public Object fetchCallback(HttpServletRequest request) {
        String callback = request.getHeader("X-Callback-Url");
        return restTemplate.getForObject(callback, String.class);
    }

    public Object fetchAnnotatedHeader(
            @RequestHeader(name = "X-Callback-Url", required = false) String callback) {
        return restTemplate.getForObject(callback, String.class);
    }

    public Object openStream(HttpServletRequest request) throws IOException {
        String next = request.getParameter("next");
        return new URL(next).openStream();
    }

    public HttpResponse<String> fetchByHost(HttpServletRequest request)
            throws IOException, InterruptedException {
        String host = request.getParameter("host");
        URI target = URI.create("https://" + host + "/internal/status");
        return httpClient.send(HttpRequest.newBuilder(target).GET().build(),
                HttpResponse.BodyHandlers.ofString());
    }

    public HttpResponse<String> fetchInboundHost(HttpServletRequest request)
            throws IOException, InterruptedException {
        String target = "https://" + request.getServerName() + "/internal/status";
        return httpClient.send(HttpRequest.newBuilder(URI.create(target)).GET().build(),
                HttpResponse.BodyHandlers.ofString());
    }
}
