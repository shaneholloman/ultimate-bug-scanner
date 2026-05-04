import java.util.UUID
import java.util.concurrent.ThreadLocalRandom
import kotlin.random.Random

class BuggyKotlinRandomSecurity {
    private val rng = Random(System.currentTimeMillis().toInt())

    fun sessionToken(userId: String): String {
        return "$userId-${rng.nextLong()}"
    }

    fun csrfNonce(): String {
        return Random.nextLong().toString(36)
    }

    fun apiKey(): String {
        return "ak_${ThreadLocalRandom.current().nextInt(1_000_000)}"
    }

    fun passwordResetToken(): String {
        return "reset_${System.currentTimeMillis().toString(36)}"
    }

    fun inviteCode(): String {
        return UUID.randomUUID().toString()
    }

    fun oneTimePassword(): String {
        return Random.Default.nextInt(100000, 999999).toString()
    }
}

