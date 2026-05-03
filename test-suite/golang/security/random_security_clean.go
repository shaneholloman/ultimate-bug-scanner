package security

import (
	cryptoRand "crypto/rand"
	"encoding/base64"
	"encoding/hex"
	"fmt"
	"io"
	mathrand "math/rand"
)

func ResetToken() string {
	buf := make([]byte, 32)
	if _, err := io.ReadFull(cryptoRand.Reader, buf); err != nil {
		panic(err)
	}
	return base64.RawURLEncoding.EncodeToString(buf)
}

func SessionSecret() string {
	buf := make([]byte, 32)
	if _, err := cryptoRand.Read(buf); err != nil {
		panic(err)
	}
	return hex.EncodeToString(buf)
}

func CSRFNonce() string {
	return ResetToken()
}

func APIKey() string {
	return fmt.Sprintf("ak_%s", SessionSecret())
}

func PickDisplayTheme() string {
	themes := []string{"light", "dark", "system"}
	return themes[mathrand.Intn(len(themes))]
}
