package security;

import java.io.IOException;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.servlet.ModelAndView;
import org.springframework.web.servlet.view.RedirectView;

public final class OpenRedirectBuggy {
    public void redirectFromQuery(HttpServletRequest request, HttpServletResponse response)
            throws IOException {
        String next = request.getParameter("next");
        response.sendRedirect(next);
    }

    public String springRedirect(@RequestParam("next") String next) {
        return "redirect:" + next;
    }

    public RedirectView redirectFromHeader(HttpServletRequest request) {
        String target = request.getHeader("X-Return-To");
        return new RedirectView(target);
    }

    public ModelAndView modelAndViewRedirect(HttpServletRequest request) {
        String location = request.getParameter("return_to");
        return new ModelAndView("redirect:" + location);
    }

    public ResponseEntity<Void> locationHeader(HttpServletRequest request) {
        String target = request.getParameter("continue");
        return ResponseEntity.status(302).header("Location", target).build();
    }
}
