using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Primitives;

public sealed class OpenRedirectBuggy : Controller
{
    public IActionResult RedirectQuery(HttpRequest request)
    {
        var target = request.Query["returnUrl"];
        return Redirect(target!);
    }

    public void ResponseRedirect(HttpContext context)
    {
        var next = context.Request.Query["next"];
        context.Response.Redirect(next!);
    }

    public IActionResult RedirectHeader(HttpContext context)
    {
        context.Request.Headers.TryGetValue("X-Return-To", out StringValues target);
        return new RedirectResult(target.ToString());
    }

    public void WriteLocationHeader(HttpContext context)
    {
        var destination = context.Request.Cookies["destination"];
        context.Response.Headers["Location"] = destination!;
    }

    public IActionResult RedirectRouteValue(HttpRequest request)
    {
        var callback = request.RouteValues["callback"]?.ToString();
        return RedirectPermanent(callback!);
    }
}
