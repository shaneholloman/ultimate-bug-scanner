import java.security.SecureRandom
import java.util.Base64
import kotlin.random.Random

class CleanKotlinRandomSecurity {
    private val secureRandom = SecureRandom()

    fun secureToken(): String {
        val bytes = ByteArray(32)
        secureRandom.nextBytes(bytes)
        return Base64.getUrlEncoder().withoutPadding().encodeToString(bytes)
    }

    fun sessionToken(): String {
        return secureToken()
    }

    fun csrfNonce(): String {
        return secureToken()
    }

    fun passwordResetToken(): String {
        return secureToken()
    }

    fun apiKey(): String {
        return "ak_${secureToken()}"
    }

    fun displayJitterBucket(): Int {
        val uiRandom = Random(42)
        return uiRandom.nextInt(8)
    }
}

