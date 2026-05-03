#include <cstdlib>
#include <map>
#include <string>

struct Request {
    std::string get_param_value(const std::string& name) const {
        return name == "filename" ? "report.csv\r\nSet-Cookie: admin=1" : "alice";
    }

    std::string getHeader(const std::string& name) const {
        return name == "X-Trace-Id" ? "trace\r\nX-Injected: yes" : "text/plain";
    }
};

struct Response {
    void set_header(const std::string& name, const std::string& value);
    void addHeader(const std::string& name, const std::string& value);
    void setContentType(const std::string& value);
};

int cgiFormString(const char *name, char *dst, int len);
void FCGX_FPrintF(void *out, const char *format, const char *value);

void display_name(const Request& req, Response& response) {
    auto name = req.get_param_value("display_name");
    response.set_header("X-Display-Name", name);
}

void download_filename(const Request& req, Response& response) {
    std::string filename = req.get_param_value("filename");
    response.addHeader("Content-Disposition", "attachment; filename=\"" + filename + "\"");
}

void upstream_trace(const Request& req, Response& response) {
    const std::string trace = req.getHeader("X-Trace-Id");
    response.set_header("X-Upstream-Trace", trace);
}

void content_type_from_header(const Request& req, Response& response) {
    auto content_type = req.getHeader("X-Content-Type");
    response.setContentType(content_type);
}

void header_map_from_cookie(std::map<std::string, std::string>& headers) {
    const char *raw = getenv("HTTP_COOKIE");
    std::string export_name = raw ? raw : "report";
    headers["X-Export-Name"] = export_name;
}

void cgi_header(Response& response) {
    char tenant[512];
    cgiFormString("tenant", tenant, sizeof(tenant));
    response.set_header("X-Tenant", tenant);
}

void raw_fcgi_header(void *out) {
    const char *trace = getenv("HTTP_X_TRACE_ID");
    FCGX_FPrintF(out, "X-Trace-Id: %s\r\n", trace);
}
