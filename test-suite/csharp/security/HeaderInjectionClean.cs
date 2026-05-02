using System;
using System.Net;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Primitives;

public sealed class HeaderInjectionClean : Controller
{
    private static string SafeHeaderValue(string raw)
    {
        return raw.Replace("\r", string.Empty).Replace("\n", string.Empty);
    }

    public void QueryValueInSafeHeader(HttpContext context)
    {
        var displayName = SafeHeaderValue(context.Request.Query["name"]!);
        context.Response.Headers["X-Display-Name"] = displayName;
    }

    public void EncodedFilenameDisposition(HttpContext context)
    {
        var filename = WebUtility.UrlEncode(context.Request.Form["filename"]!);
        context.Response.Headers.Append("Content-Disposition", "attachment; filename=" + filename);
    }

    public IActionResult GuardedRequestHeader(HttpContext context)
    {
        context.Request.Headers.TryGetValue("X-Trace-ID", out StringValues traceId);
        var trace = traceId.ToString();
        if (trace.Contains("\r", StringComparison.Ordinal) ||
            trace.Contains("\n", StringComparison.Ordinal))
        {
            return BadRequest();
        }

        context.Response.Headers.Add("X-Upstream-Trace", trace);
        return Ok();
    }

    public void AnnotatedQueryParameter([FromQuery] string reason)
    {
        Response.Headers.Set("X-Return-Reason", SafeHeaderValue(reason));
    }
}
