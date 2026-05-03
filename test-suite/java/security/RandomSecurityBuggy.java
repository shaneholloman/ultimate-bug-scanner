import java.util.Random;
import java.util.SplittableRandom;
import java.util.concurrent.ThreadLocalRandom;

class RandomSecurityBuggy {
    private final Random rng = new Random();

    String resetToken() {
        long token = rng.nextLong();
        return Long.toString(token, 36);
    }

    String sessionSecret() {
        Random local = new Random(System.currentTimeMillis());
        return "sess_" + Long.toString(local.nextLong(), 36);
    }

    String csrfNonce() {
        String nonce = Long.toString(System.currentTimeMillis(), 36);
        return "csrf_" + nonce;
    }

    String apiKey() {
        return "ak_" + ThreadLocalRandom.current().nextInt(1_000_000);
    }

    String oneTimePassword() {
        int otp = new SplittableRandom().nextInt(100000, 1000000);
        return String.format("%06d", otp);
    }

    String inviteToken() {
        return Long.toString((long) (Math.random() * Long.MAX_VALUE), 36);
    }
}
