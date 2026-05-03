import java.security.SecureRandom;
import java.util.Base64;
import java.util.Random;

class RandomSecurityClean {
    private static final SecureRandom SECURE_RANDOM = new SecureRandom();

    String resetToken() {
        byte[] bytes = new byte[32];
        SECURE_RANDOM.nextBytes(bytes);
        return Base64.getUrlEncoder().withoutPadding().encodeToString(bytes);
    }

    String sessionSecret() {
        return resetToken();
    }

    String csrfNonce() {
        return resetToken();
    }

    String apiKey() {
        return "ak_" + resetToken();
    }

    String pickDisplayTheme() {
        Random displayRandom = new Random(42);
        return new String[] {"light", "dark", "system"}[displayRandom.nextInt(3)];
    }
}
