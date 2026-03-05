using System;
using System.Collections.Generic;

public static class TypeNarrowingBuggy
{
    public static int Run(string rawInput, Dictionary<string, string> cache)
    {
        if (rawInput == null)
        {
            Console.WriteLine("missing input");
        }

        if (!cache.TryGetValue("token", out var token))
        {
            Console.WriteLine("missing token");
        }

        return rawInput.Trim().Length + token.Length;
    }
}
