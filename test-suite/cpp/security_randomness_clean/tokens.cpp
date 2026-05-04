#include <array>
#include <cstdlib>
#include <iomanip>
#include <sstream>
#include <string>
#include <vector>

extern "C" int RAND_bytes(unsigned char *buf, int num);

int displayJitterBucket() {
    return std::rand() % 8;
}

std::string hexEncode(const std::vector<unsigned char> &bytes) {
    std::ostringstream out;
    for (unsigned char byte : bytes) {
        out << std::hex << std::setw(2) << std::setfill('0') << static_cast<int>(byte);
    }
    return out.str();
}

std::string secureToken() {
    std::vector<unsigned char> bytes(32);
    if (RAND_bytes(bytes.data(), static_cast<int>(bytes.size())) != 1) {
        return {};
    }
    return hexEncode(bytes);
}

std::string makeSessionToken() {
    return secureToken();
}

std::string csrfNonce() {
    return secureToken();
}

std::string passwordResetToken() {
    return secureToken();
}

const char *securityRandomnessGuidance() {
    return "Tokens must not use rand() or std::mt19937.";
}

/*
 * Reset tokens, invite codes, and API keys must not be generated with rand().
 */
