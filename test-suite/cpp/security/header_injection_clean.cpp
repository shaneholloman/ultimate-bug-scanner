#include <cstdlib>
#include <map>
#include <stdexcept>
#include <string>

struct Request {
    std::string get_param_value(const std::string& name) const {
        return name == "filename" ? "report.csv" : "alice";
    }

    std::string getHeader(const std::string& name) const {
        return name == "X-Trace-Id" ? "trace-123" : "text/plain";
    }
};

struct Response {
    void set_header(const std::string& name, const std::string& value);
    void addHeader(const std::string& name, const std::string& value);
    void setContentType(const std::string& value);
};

std::string safe_header_value(std::string value) {
    for (char& ch : value) {
        if (ch == '\r' || ch == '\n') {
            ch = ' ';
        }
    }
    return value;
}

std::string encoded_filename(const std::string& value) {
    return safe_header_value(value);
}

std::string reject_crlf(const std::string& value) {
    if (value.find('\r') != std::string::npos || value.find('\n') != std::string::npos) {
        throw std::invalid_argument("invalid header value");
    }
    return value;
}

void display_name(const Request& req, Response& response) {
    auto name = safe_header_value(req.get_param_value("display_name"));
    response.set_header("X-Display-Name", name);
}

void download_filename(const Request& req, Response& response) {
    std::string filename = encoded_filename(req.get_param_value("filename"));
    response.addHeader("Content-Disposition", "attachment; filename=\"" + filename + "\"");
}

void upstream_trace(const Request& req, Response& response) {
    const std::string trace = reject_crlf(req.getHeader("X-Trace-Id"));
    response.set_header("X-Upstream-Trace", trace);
}

void content_type_from_header(const Request& req, Response& response) {
    auto content_type = safe_header_value(req.getHeader("X-Content-Type"));
    response.setContentType(content_type);
}

void header_map_from_cookie(std::map<std::string, std::string>& headers) {
    const char *raw = getenv("HTTP_COOKIE");
    std::string export_name = safe_header_value(raw ? raw : "report");
    headers["X-Export-Name"] = export_name;
}
