import CryptoKit
import Foundation
import Security

func createSessionToken() -> String {
    var bytes = [UInt8](repeating: 0, count: 32)
    let status = SecRandomCopyBytes(kSecRandomDefault, bytes.count, &bytes)
    guard status == errSecSuccess else {
        return ""
    }
    return Data(bytes).base64EncodedString()
}

func csrfNonce() -> String {
    let key = SymmetricKey(size: .bits256)
    return key.withUnsafeBytes { rawBuffer in
        Data(rawBuffer).base64EncodedString()
    }
}

func issueApiKey() -> String {
    return secureToken()
}

func secureToken() -> String {
    var bytes = [UInt8](repeating: 0, count: 24)
    guard SecRandomCopyBytes(kSecRandomDefault, bytes.count, &bytes) == errSecSuccess else {
        return ""
    }
    return Data(bytes).base64EncodedString()
}

func displayJitterBucket() -> Int {
    return Int.random(in: 0..<8)
}

let documentation = "Security tokens must not use Int.random(in:) or arc4random_uniform."
