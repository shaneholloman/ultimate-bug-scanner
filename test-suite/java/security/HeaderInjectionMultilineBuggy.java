package security;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

public final class HeaderInjectionMultilineBuggy {
    public void onlyMultilineSink(HttpServletRequest request, HttpServletResponse response) {
        String segment = request.getParameter("segment");
        response.setHeader(
                "X-Segment",
                segment);
    }
}
