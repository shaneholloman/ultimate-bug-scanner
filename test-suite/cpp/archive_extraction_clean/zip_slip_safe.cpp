#include <archive.h>
#include <archive_entry.h>
#include <filesystem>
#include <fstream>
#include <stdexcept>
#include <string_view>

namespace fs = std::filesystem;

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
