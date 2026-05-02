using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Primitives;

public sealed class HeaderInjectionBuggy : Controller
{
    public void QueryValueInHeader(HttpContext context)
    {
        var displayName = context.Request.Query["name"];
        context.Response.Headers["X-Display-Name"] = displayName!;
    }

    public void RequestFilenameInDisposition(HttpContext context)
    {
        var filename = context.Request.Form["filename"];
        context.Response.Headers.Append("Content-Disposition", "attachment; filename=" + filename);
    }

    public void RequestHeaderReflected(HttpContext context)
    {
        context.Request.Headers.TryGetValue("X-Trace-ID", out StringValues traceId);
        context.Response.Headers.Add("X-Upstream-Trace", traceId.ToString());
    }

    public void AnnotatedQueryParameter([FromQuery] string reason)
    {
        Response.Headers.Set("X-Return-Reason", reason);
    }

    public void TypedContentDisposition(HttpContext context)
    {
        var attachment = context.Request.Query["attachment"].ToString();
        context.Response.GetTypedHeaders().ContentDisposition =
            new System.Net.Http.Headers.ContentDispositionHeaderValue("attachment")
            {
                FileName = attachment
            };
    }
}
