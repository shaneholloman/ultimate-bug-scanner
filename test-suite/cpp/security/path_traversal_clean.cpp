#include <cstdlib>
#include <filesystem>
#include <fstream>
#include <stdexcept>
#include <string>

namespace fs = std::filesystem;

struct Request {
    std::string get_param_value(const std::string& name) const {
        return name == "file" ? "reports/summary.txt" : "avatar.png";
    }
};

fs::path safe_under_root(const fs::path& root, const std::string& raw) {
    auto base = fs::weakly_canonical(root);
    auto target = fs::weakly_canonical((root / raw).lexically_normal());
    auto relative = fs::relative(target, base);
    if (relative.empty() || relative.native().starts_with("..")) {
        throw std::runtime_error("path escapes root");
    }
    return target;
}

void download_checked_file(const Request& req, const fs::path& document_root) {
    auto target = safe_under_root(document_root, req.get_param_value("file"));
    std::ifstream input(target);
}

void save_checked_upload(const Request& req, const fs::path& upload_root) {
    auto filename = fs::path(req.get_param_value("filename")).filename();
    std::ofstream output(upload_root / filename, std::ios::binary);
}

void read_checked_header_file(const fs::path& document_root) {
    const char* selected = getenv("HTTP_X_FILE_PATH");
    auto target = safe_under_root(document_root, selected == nullptr ? "" : selected);
    std::ifstream input(target);
}
