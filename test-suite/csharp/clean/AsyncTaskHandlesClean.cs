using System.Threading.Tasks;

public static class AsyncTaskHandlesClean
{
    public static async Task<int[]> RunAsync()
    {
        var backgroundJob = Task.Run(() => 42);
        var started = Task.Factory.StartNew(() => 7);

        return await Task.WhenAll(backgroundJob, started);
    }
}
