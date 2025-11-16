#include <array>
#include <cstring>
#include <iostream>
#include <memory>
#include <mutex>
#include <string>

std::unique_ptr<char[]> copy_safely(const std::string &input) {
    auto buf = std::make_unique<char[]>(input.size() + 1);
    std::strncpy(buf.get(), input.c_str(), input.size());
    buf[input.size()] = '\0';
    return buf;
}

class ScopedLock {
public:
    explicit ScopedLock(std::mutex &m) : m_(m) { m_.lock(); }
    ~ScopedLock() { m_.unlock(); }

private:
    std::mutex &m_;
};

int main() {
    auto safe = copy_safely("hello world");
    std::cout << safe.get() << "\n";

    std::mutex m;
    ScopedLock lock{m};
    // protected critical section
    return 0;
}
