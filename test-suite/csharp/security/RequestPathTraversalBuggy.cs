using System.IO;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;

public sealed class RequestPathTraversalBuggy : ControllerBase
{
    private const string Root = "/srv/app/files";

    public string ReadReport(HttpRequest request)
    {
        var name = request.Query["file"];
        var target = Path.Combine(Root, name!);
        return System.IO.File.ReadAllText(target);
    }

    public IActionResult Download(HttpContext httpContext)
    {
        var requested = httpContext.Request.Path.Value!;
        return PhysicalFile(Path.Combine(Root, requested), "application/octet-stream");
    }

    public void SaveUpload(IFormFile upload)
    {
        var filename = upload.FileName;
        var target = Path.Combine(Root, filename);
        using var output = new FileStream(target, FileMode.Create);
        upload.CopyTo(output);
    }

    public void DeleteExport(HttpRequest request)
    {
        var target = Path.Combine(Root, request.Form["delete"]);
        System.IO.File.Delete(target);
    }

    public string ReadHeaderSelection(HttpContext context)
    {
        context.Request.Headers.TryGetValue("X-File-Path", out var requested);
        var target = Path.Combine(Root, requested!);
        return System.IO.File.ReadAllText(target);
    }
}
