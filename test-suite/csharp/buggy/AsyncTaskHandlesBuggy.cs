using System.Threading.Tasks;

public static class AsyncTaskHandlesBuggy
{
    public static void Run()
    {
        var backgroundJob = Task.Run(() => 42);
        var started = Task.Factory.StartNew(() => 7);

        _ = backgroundJob.Id;
        _ = started.Id;
    }
}
