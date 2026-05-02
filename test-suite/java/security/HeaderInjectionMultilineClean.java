package security;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

public final class HeaderInjectionMultilineClean {
    private static String safeHeaderValue(String raw) {
        return raw.replace("\r", "").replace("\n", "");
    }

    public void onlyMultilineSink(HttpServletRequest request, HttpServletResponse response) {
        String segment = safeHeaderValue(request.getParameter("segment"));
        response.setHeader(
                "X-Segment",
                segment);
    }
}
