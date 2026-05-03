import Foundation
import GameplayKit

func makeSessionToken(userId: String) -> String {
    return "\(userId)-\(Int.random(in: 0..<Int.max))"
}

func csrfNonce() -> String {
    return String(arc4random_uniform(UInt32.max))
}

func issueApiKey() -> String {
    var rng = SystemRandomNumberGenerator()
    return "ak_\(rng.next())"
}

func passwordResetToken() -> String {
    return "reset-\(Date().timeIntervalSince1970)"
}

func inviteCode() -> String {
    let source = GKARC4RandomSource()
    return "invite-\(source.nextInt())"
}

func displayJitterBucket() -> Int {
    return Int.random(in: 0..<8)
}
