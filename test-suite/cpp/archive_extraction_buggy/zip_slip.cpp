#include <archive.h>
#include <archive_entry.h>
#include <fcntl.h>
#include <filesystem>
#include <fstream>
#include <string>
#include <zip.h>

namespace fs = std::filesystem;

using unzFile = void*;
struct unz_file_info {};
int unzGetCurrentFileInfo(
    unzFile file,
    unz_file_info* info,
    char* filename_inzip,
    unsigned long filename_size,
    void* extra_field,
    unsigned long extra_field_size,
    void* comment,
    unsigned long comment_size);

struct mz_zip_archive {};
struct mz_zip_archive_file_stat {
    const char* m_filename;
};
bool mz_zip_reader_file_stat(mz_zip_archive* archive, unsigned int index, mz_zip_archive_file_stat* stat);

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

void extract_minizip_unsafe(unzFile file, const fs::path& destination) {
    char filename_inzip[256] = {};
    unz_file_info info{};
    unzGetCurrentFileInfo(file, &info, filename_inzip, sizeof(filename_inzip), nullptr, 0, nullptr, 0);
    auto target = destination / filename_inzip;
    std::ofstream out(target, std::ios::binary);
}

void extract_miniz_unsafe(mz_zip_archive& archive, const fs::path& destination, unsigned int index) {
    mz_zip_archive_file_stat file_stat{};
    if (mz_zip_reader_file_stat(&archive, index, &file_stat)) {
        auto target = destination / file_stat.m_filename;
        std::ofstream out(target, std::ios::binary);
    }
}
