using System.IO;
using System.Net.Http;
using System.Threading;

public static class ResourceLifecycleClean
{
    public static void Tidy()
    {
        using var cts = new CancellationTokenSource();
        using var reader = new StreamReader(new MemoryStream());
        using var request = new HttpRequestMessage(HttpMethod.Get, "https://example.com");

        cts.CancelAfter(5);
        _ = reader.Peek();
        _ = request.Method;
    }
}
