#include <archive.h>
#include <archive_entry.h>
#include <fcntl.h>
#include <filesystem>
#include <fstream>
#include <string>
#include <zip.h>

namespace fs = std::filesystem;

void extract_libarchive_unsafe(archive* ar, archive_entry* entry, const fs::path& destination) {
    const char* entry_name = archive_entry_pathname(entry);
    fs::path target = destination / entry_name;
    std::ofstream out(target, std::ios::binary);
    (void)ar;
}

void extract_libzip_unsafe(zip_t* zip, const fs::path& destination, zip_uint64_t index) {
    const char* name = zip_get_name(zip, index, 0);
    auto target = destination / name;
    FILE* output = fopen(target.string().c_str(), "wb");
    if (output != nullptr) {
        fclose(output);
    }
}

void extract_string_concat_unsafe(const std::string& destination, archive_entry* entry) {
    std::string target = destination + "/" + archive_entry_pathname(entry);
    int fd = ::open(target.c_str(), O_CREAT | O_WRONLY, 0600);
    (void)fd;
}
