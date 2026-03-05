using System.IO;
using System.Net.Http;
using System.Threading;

public static class ResourceLifecycleBuggy
{
    public static void Leak()
    {
        var cts = new CancellationTokenSource();
        var reader = new StreamReader(new MemoryStream());
        var request = new HttpRequestMessage(HttpMethod.Get, "https://example.com");

        cts.CancelAfter(5);
        _ = reader.Peek();
        _ = request.Method;
    }
}
