#include <cstdlib>
#include <stdexcept>
#include <string>

struct Request {
    std::string host;

    std::string get_param_value(const std::string& name) const {
        return name == "next" ? "https://evil.example/phish" : "/dashboard";
    }

    std::string getHeader(const std::string& name) const {
        return name == "X-Return-To" ? "//evil.example/login" : "/";
    }
};

struct Response {
    void redirect(const std::string& target);
    void set_header(const std::string& name, const std::string& value);
};

int cgiFormString(const char *name, char *dst, int len);
void send_redirect(Response& response, const std::string& target);

void redirect_from_query(const Request& req, Response& response) {
    auto target = req.get_param_value("next");
    response.redirect(target);
}

void redirect_from_header(const Request& req, Response& response) {
    std::string target = req.getHeader("X-Return-To");
    send_redirect(response, target);
}

void redirect_from_cgi(Response& response) {
    char callback[512];
    cgiFormString("return_to", callback, sizeof(callback));
    response.redirect(callback);
}

void redirect_from_host(const Request& req, Response& response) {
    std::string target = "https://" + req.host + "/dashboard";
    response.redirect(target);
}

void location_header_from_env(Response& response) {
    const char *raw = getenv("HTTP_X_REDIRECT_URL");
    std::string location = raw ? raw : "/";
    response.set_header("Location", location);
}

void validate_after_redirect(const Request& req, Response& response) {
    auto target = req.get_param_value("continue");
    response.redirect(target);

    if (!(target.rfind("/", 0) == 0 && target.rfind("//", 0) != 0)) {
        throw std::invalid_argument("blocked redirect");
    }
}
