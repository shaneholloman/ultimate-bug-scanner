#include <cstdio>
#include <cstdlib>
#include <filesystem>
#include <fstream>
#include <string>

namespace fs = std::filesystem;

struct Request {
    std::string path;

    std::string get_param_value(const std::string& name) const {
        return name == "file" ? "../secrets.txt" : "../avatar.png";
    }
};

void download_query_file(const Request& req, const fs::path& document_root) {
    auto name = req.get_param_value("file");
    std::ifstream input(document_root / name);
}

void serve_raw_request_path(const Request& req, const fs::path& document_root) {
    auto target = document_root / req.path;
    FILE* file = fopen(target.string().c_str(), "rb");
    if (file != nullptr) {
        fclose(file);
    }
}

void save_upload_filename(const Request& req, const fs::path& upload_root) {
    auto filename = req.get_param_value("filename");
    std::ofstream output(upload_root / filename, std::ios::binary);
}

void delete_cgi_selected_file(const fs::path& upload_root) {
    const char* selected = getenv("QUERY_STRING");
    auto target = upload_root / selected;
    fs::remove(target);
}
