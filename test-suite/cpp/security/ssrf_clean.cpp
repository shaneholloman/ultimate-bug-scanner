#include <cstdlib>
#include <stdexcept>
#include <string>
#include <unordered_set>

using CURL = void;

enum CurlOpt {
    CURLOPT_URL
};

void curl_easy_setopt(CURL *handle, CurlOpt option, const std::string &value);

std::string safe_outbound_url(const char *raw) {
    const std::string value = raw ? raw : "https://api.example.com";
    const std::unordered_set<std::string> allowed_hosts = {
        "api.example.com",
        "hooks.example.com"
    };

    const std::string prefix = "https://";
    if (value.rfind(prefix, 0) != 0) {
        throw std::invalid_argument("blocked scheme");
    }

    const auto host_end = value.find('/', prefix.size());
    const std::string host = value.substr(prefix.size(), host_end - prefix.size());
    if (allowed_hosts.find(host) == allowed_hosts.end()) {
        throw std::invalid_argument("blocked host");
    }
    return value;
}

void fetch_from_query(CURL *curl) {
    const std::string target = safe_outbound_url(getenv("QUERY_STRING"));
    curl_easy_setopt(curl, CURLOPT_URL, target);
}

void fetch_from_header(CURL *curl) {
    const std::string callback = safe_outbound_url(getenv("HTTP_X_CALLBACK_URL"));
    curl_easy_setopt(curl, CURLOPT_URL, callback);
}
