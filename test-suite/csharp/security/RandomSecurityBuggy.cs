using System;
using System.Diagnostics;

public sealed class RandomSecurityBuggy
{
    private readonly Random rng = new Random();

    public string ResetToken()
    {
        long token = rng.NextInt64();
        return token.ToString("x");
    }

    public string SessionSecret()
    {
        var local = new Random(Environment.TickCount);
        return "sess_" + local.NextInt64().ToString("x");
    }

    public string CsrfNonce()
    {
        string nonce = DateTime.UtcNow.Ticks.ToString("x");
        return "csrf_" + nonce;
    }

    public string ApiKey()
    {
        return "ak_" + Random.Shared.Next(1_000_000);
    }

    public string OneTimePassword()
    {
        return new Random().Next(100000, 999999).ToString();
    }

    public string InviteToken()
    {
        return Guid.NewGuid().ToString("N");
    }

    public string RecoverySecret()
    {
        return "r_" + Process.GetCurrentProcess().Id.ToString("x");
    }
}
