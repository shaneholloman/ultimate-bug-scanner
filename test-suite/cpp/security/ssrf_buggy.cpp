#include <cstdlib>
#include <string>

using CURL = void;

enum CurlOpt {
    CURLOPT_URL
};

void curl_easy_setopt(CURL *handle, CurlOpt option, const char *value);
void curl_easy_setopt(CURL *handle, CurlOpt option, const std::string &value);
int cgiFormString(const char *name, char *dst, int len);

void fetch_from_query(CURL *curl) {
    const char *raw = getenv("QUERY_STRING");
    std::string target = raw ? raw : "https://example.com";
    curl_easy_setopt(curl, CURLOPT_URL, target.c_str());
}

void fetch_from_header(CURL *curl) {
    const char *raw = getenv("HTTP_X_CALLBACK_URL");
    std::string callback = raw ? raw : "https://example.com";
    curl_easy_setopt(curl, CURLOPT_URL, callback);
}

void fetch_from_cgi_form(CURL *curl) {
    char callback[512];
    cgiFormString("callback", callback, sizeof(callback));
    curl_easy_setopt(curl, CURLOPT_URL, callback);
}
