package security

import (
	"fmt"
	mathrand "math/rand"
	"os"
	"strconv"
	"time"
)

func ResetToken() string {
	token := mathrand.Int63()
	return strconv.FormatInt(token, 36)
}

func SessionSecret() string {
	secret := mathrand.New(mathrand.NewSource(time.Now().UnixNano())).Int63()
	return fmt.Sprintf("sess_%d", secret)
}

func CSRFNonce() string {
	nonce := fmt.Sprintf("%d", time.Now().UnixNano())
	return "csrf_" + nonce
}

func RecoveryCode() int64 {
	recovery := time.Now().UnixNano()
	return recovery
}

func APIKey() string {
	return fmt.Sprintf("ak_%d_%d", os.Getpid(), mathrand.Intn(1_000_000))
}

func OneTimePassword() string {
	rng := mathrand.New(mathrand.NewSource(time.Now().UnixNano()))
	otp := rng.Intn(900000) + 100000
	return fmt.Sprintf("%06d", otp)
}
