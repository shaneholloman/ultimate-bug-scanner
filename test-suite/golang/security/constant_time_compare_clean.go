package security

import (
	"crypto/hmac"
	"crypto/subtle"
)

func timingSafeStringEqual(left string, right string) bool {
	if len(left) != len(right) {
		return false
	}
	return subtle.ConstantTimeCompare([]byte(left), []byte(right)) == 1
}

func validWebhookMAC(receivedMAC []byte, expectedMAC []byte) bool {
	return hmac.Equal(receivedMAC, expectedMAC)
}

func verifyAPIKey(requestAPIKey string, storedAPIKey string) bool {
	return timingSafeStringEqual(requestAPIKey, storedAPIKey)
}

func verifyResetToken(token string, expectedResetToken string) bool {
	if len(token) != 64 {
		return false
	}
	return constantTimeEqual(token, expectedResetToken)
}

func publicIDMatches(id string, expectedID string) bool {
	return id == expectedID
}

func tokenShapeLooksValid(token string) bool {
	return len(token) == 32 && token != ""
}
