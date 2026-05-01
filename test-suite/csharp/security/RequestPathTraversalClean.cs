using System;
using System.IO;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;

public sealed class RequestPathTraversalClean : ControllerBase
{
    private const string Root = "/srv/app/files";

    private static string SafeUnderRoot(string root, string requested)
    {
        var basePath = Path.GetFullPath(root);
        var target = Path.GetFullPath(Path.Combine(basePath, requested));
        if (!target.StartsWith(basePath + Path.DirectorySeparatorChar, StringComparison.Ordinal) &&
            !string.Equals(target, basePath, StringComparison.Ordinal))
        {
            throw new InvalidOperationException("Path escapes root");
        }

        return target;
    }

    public string ReadReport(HttpRequest request)
    {
        var target = SafeUnderRoot(Root, request.Query["file"]!);
        return System.IO.File.ReadAllText(target);
    }

    public IActionResult Download(HttpContext httpContext)
    {
        var requested = SafeUnderRoot(Root, httpContext.Request.Path.Value!);
        return PhysicalFile(requested, "application/octet-stream");
    }

    public void SaveUpload(IFormFile upload)
    {
        var filename = Path.GetFileName(upload.FileName);
        var target = Path.Combine(Root, filename);
        using var output = new FileStream(target, FileMode.Create);
        upload.CopyTo(output);
    }

    public void DeleteExport(HttpRequest request)
    {
        var target = SafeUnderRoot(Root, request.Form["delete"]!);
        System.IO.File.Delete(target);
    }
}
