using System;
using System.Security.Cryptography;

public sealed class RandomSecurityClean
{
    public string ResetToken()
    {
        return Convert.ToHexString(RandomNumberGenerator.GetBytes(32));
    }

    public string SessionSecret()
    {
        return ResetToken();
    }

    public string CsrfNonce()
    {
        return Convert.ToBase64String(RandomNumberGenerator.GetBytes(32));
    }

    public string ApiKey()
    {
        return "ak_" + RandomNumberGenerator.GetHexString(32);
    }

    public string OneTimePassword()
    {
        return RandomNumberGenerator.GetInt32(100000, 1000000).ToString();
    }

    public string PickDisplayTheme()
    {
        var displayRandom = new Random(42);
        var themes = new[] { "light", "dark", "system" };
        return themes[displayRandom.Next(themes.Length)];
    }
}
