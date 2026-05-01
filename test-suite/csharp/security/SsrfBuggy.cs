using System;
using System.Net;
using System.Net.Http;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Http;

public sealed class SsrfBuggy
{
    private readonly HttpClient _httpClient = new HttpClient();

    public Task<string> FetchQuery(HttpRequest request)
    {
        var target = request.Query["url"];
        return _httpClient.GetStringAsync(target!);
    }

    public Task<HttpResponseMessage> FetchCallback(HttpContext context)
    {
        var callback = context.Request.Headers["X-Callback-Url"];
        return _httpClient.GetAsync(callback!);
    }

    public Task<HttpResponseMessage> SendRouteEndpoint(HttpRequest request)
    {
        var endpoint = request.RouteValues["endpoint"]?.ToString();
        var message = new HttpRequestMessage(HttpMethod.Get, endpoint);
        return _httpClient.SendAsync(message);
    }

    public WebRequest CreateWebhookRequest(HttpContext context)
    {
        var webhook = context.Request.Form["webhookUrl"];
        return WebRequest.Create(webhook!);
    }

    public string FetchHost(HttpRequest request)
    {
        var host = request.Query["host"];
        using var webClient = new WebClient();
        return webClient.DownloadString("https://" + host + "/internal/status");
    }

    public Task<HttpResponseMessage> ValidateTooLate(HttpRequest request)
    {
        var target = request.Query["lateUrl"];
        var response = _httpClient.GetAsync(target!);
        if (!Uri.TryCreate(target, UriKind.Absolute, out var uri) || uri.Host != "api.example.com")
        {
            return Task.FromResult(new HttpResponseMessage(HttpStatusCode.BadRequest));
        }

        return response;
    }
}
