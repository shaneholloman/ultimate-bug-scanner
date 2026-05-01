using System;
using System.Collections.Generic;
using System.Net;
using System.Net.Http;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Http;

public sealed class SsrfClean
{
    private static readonly HashSet<string> AllowedHosts = new(StringComparer.OrdinalIgnoreCase)
    {
        "api.example.com",
        "hooks.example.com"
    };

    private readonly HttpClient _httpClient = new HttpClient();

    private static Uri SafeOutboundUrl(string raw)
    {
        if (!Uri.TryCreate(raw, UriKind.Absolute, out var uri) ||
            uri.Scheme != Uri.UriSchemeHttps ||
            !AllowedHosts.Contains(uri.Host))
        {
            throw new InvalidOperationException("blocked outbound URL");
        }

        return uri;
    }

    public Task<string> FetchQuery(HttpRequest request)
    {
        var target = SafeOutboundUrl(request.Query["url"]!);
        return _httpClient.GetStringAsync(target);
    }

    public Task<HttpResponseMessage> FetchCallback(HttpContext context)
    {
        var callback = SafeOutboundUrl(context.Request.Headers["X-Callback-Url"]!);
        return _httpClient.GetAsync(callback);
    }

    public Task<HttpResponseMessage> SendRouteEndpoint(HttpRequest request)
    {
        var endpoint = SafeOutboundUrl(request.RouteValues["endpoint"]?.ToString() ?? "https://api.example.com");
        var message = new HttpRequestMessage(HttpMethod.Get, endpoint);
        return _httpClient.SendAsync(message);
    }

    public WebRequest CreateWebhookRequest(HttpContext context)
    {
        var webhook = SafeOutboundUrl(context.Request.Form["webhookUrl"]!);
        return WebRequest.Create(webhook);
    }

    public string FetchHost(HttpRequest request)
    {
        var target = SafeOutboundUrl(request.Query["url"]!);
        using var webClient = new WebClient();
        return webClient.DownloadString(target);
    }

    public Task<HttpResponseMessage> FetchAfterInlineValidation(HttpRequest request)
    {
        var target = request.Query["nextUrl"].ToString();
        if (!Uri.TryCreate(target, UriKind.Absolute, out var uri) ||
            uri.Scheme != Uri.UriSchemeHttps ||
            !AllowedHosts.Contains(uri.Host))
        {
            return Task.FromResult(new HttpResponseMessage(HttpStatusCode.BadRequest));
        }

        return _httpClient.GetAsync(target);
    }
}
