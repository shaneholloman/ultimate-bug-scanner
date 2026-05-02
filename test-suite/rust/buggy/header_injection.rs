use axum::extract::Query;
use std::collections::HashMap;

const CONTENT_DISPOSITION: &str = "Content-Disposition";

struct HeaderMap;
struct HeaderValue;
struct Request;
struct Response;
struct ResponseBuilder;

impl HeaderMap {
    fn get(&self, _name: &str) -> Option<HeaderValue> {
        Some(HeaderValue)
    }

    fn insert(&mut self, _name: &str, _value: impl AsRef<str>) {}
}

impl HeaderValue {
    fn to_str(&self) -> Result<&str, ()> {
        Ok("evil\r\nSet-Cookie: session=stolen")
    }
}

impl Request {
    fn headers(&self) -> HeaderMap {
        HeaderMap
    }
}

impl Response {
    fn builder() -> ResponseBuilder {
        ResponseBuilder
    }
}

impl ResponseBuilder {
    fn header(self, _name: &str, _value: impl AsRef<str>) -> Self {
        self
    }
}

fn query_value_in_header(Query(params): Query<HashMap<String, String>>) -> ResponseBuilder {
    let display_name = params.get("name").cloned().unwrap_or_default();
    Response::builder().header("X-Display-Name", display_name)
}

fn filename_in_content_disposition(Query(params): Query<HashMap<String, String>>) -> ResponseBuilder {
    let filename = params.get("filename").cloned().unwrap_or_default();
    Response::builder().header(CONTENT_DISPOSITION, format!("attachment; filename={filename}"))
}

fn request_header_reflected(req: Request) -> ResponseBuilder {
    let trace_id = req
        .headers()
        .get("x-trace-id")
        .and_then(|value| value.to_str().ok())
        .unwrap_or_default();
    Response::builder().header("X-Upstream-Trace", trace_id)
}

fn mutable_header_map(Query(params): Query<HashMap<String, String>>, mut response_headers: HeaderMap) {
    let mode = params.get("mode").cloned().unwrap_or_default();
    response_headers.insert("X-Mode", mode);
}

fn validate_after_setting(Query(params): Query<HashMap<String, String>>) -> Result<ResponseBuilder, &'static str> {
    let reason = params.get("reason").cloned().unwrap_or_default();
    let response = Response::builder().header("X-Return-Reason", &reason);
    if reason.contains('\r') || reason.contains('\n') {
        return Err("invalid header");
    }
    Ok(response)
}
