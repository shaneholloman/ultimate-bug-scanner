#include <chrono>
#include <cstdlib>
#include <ctime>
#include <random>
#include <string>
#include <unistd.h>

std::string makeSessionToken(const std::string &user_id) {
    return user_id + "-" + std::to_string(std::rand());
}

std::string csrfNonce() {
    return std::to_string(random());
}

std::string issueApiKey() {
    std::mt19937 rng(static_cast<unsigned>(std::time(nullptr)));
    std::uniform_int_distribution<int> dist(0, 999999);
    return "ak_" + std::to_string(dist(rng));
}

std::string emailVerificationToken() {
    std::random_device rd;
    return "verify-" + std::to_string(rd());
}

std::string passwordResetToken() {
    auto now = std::chrono::system_clock::now().time_since_epoch().count();
    return "reset-" + std::to_string(now);
}

std::string inviteCode() {
    return "invite-" + std::to_string(getpid());
}
