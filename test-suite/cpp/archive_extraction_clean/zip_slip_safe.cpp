#include <archive.h>
#include <archive_entry.h>
#include <filesystem>
#include <fstream>
#include <stdexcept>
#include <string_view>

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

fs::path safe_archive_path(const fs::path& destination, std::string_view entry_name) {
    auto root = fs::weakly_canonical(destination);
    auto target = fs::weakly_canonical((destination / entry_name).lexically_normal());
    auto relative = fs::relative(target, root);
    if (relative.empty() || relative.native().starts_with("..")) {
        throw std::runtime_error("archive entry escapes destination");
    }
    return target;
}

void extract_libarchive_safe(archive* ar, archive_entry* entry, const fs::path& destination) {
    auto entry_name = archive_entry_pathname(entry);
    auto target = safe_archive_path(destination, entry_name);
    std::ofstream out(target, std::ios::binary);
    (void)ar;
}

bool inside_destination(const fs::path& destination, const fs::path& target) {
    auto root = fs::weakly_canonical(destination);
    auto resolved = fs::weakly_canonical(target);
    auto relative = fs::relative(resolved, root);
    return !relative.empty() && !relative.native().starts_with("..");
}

void extract_with_inline_check(archive_entry* entry, const fs::path& destination) {
    auto entry_name = archive_entry_pathname(entry);
    auto normalized = (destination / entry_name).lexically_normal();
    if (!inside_destination(destination, normalized)) {
        throw std::runtime_error("archive entry escapes destination");
    }
    std::ofstream out(normalized, std::ios::binary);
}

void extract_minizip_safe(unzFile file, const fs::path& destination) {
    char filename_inzip[256] = {};
    unz_file_info info{};
    unzGetCurrentFileInfo(file, &info, filename_inzip, sizeof(filename_inzip), nullptr, 0, nullptr, 0);
    auto target = safe_archive_path(destination, filename_inzip);
    std::ofstream out(target, std::ios::binary);
}

void extract_miniz_safe(mz_zip_archive& archive, const fs::path& destination, unsigned int index) {
    mz_zip_archive_file_stat file_stat{};
    if (mz_zip_reader_file_stat(&archive, index, &file_stat)) {
        auto target = safe_archive_path(destination, file_stat.m_filename);
        std::ofstream out(target, std::ios::binary);
    }
}
