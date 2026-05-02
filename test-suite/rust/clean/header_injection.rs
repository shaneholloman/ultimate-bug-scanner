use axum::extract::Query;
use http::HeaderValue;
use std::collections::HashMap;

struct Response;
struct ResponseBuilder;

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

fn safe_header_value(raw: &str) -> String {
    raw.replace('\r', "").replace('\n', "")
}

fn query_value_in_safe_header(Query(params): Query<HashMap<String, String>>) -> ResponseBuilder {
    let display_name = safe_header_value(params.get("name").map(String::as_str).unwrap_or_default());
    Response::builder().header("X-Display-Name", display_name)
}

fn encoded_filename(Query(params): Query<HashMap<String, String>>) -> ResponseBuilder {
    let filename = params.get("filename").map(String::as_str).unwrap_or_default();
    let encoded = urlencoding::encode(filename);
    Response::builder().header("Content-Disposition", format!("attachment; filename={encoded}"))
}

fn header_value_constructor(Query(params): Query<HashMap<String, String>>) -> Result<ResponseBuilder, &'static str> {
    let trace_id = params.get("trace_id").map(String::as_str).unwrap_or_default();
    let header = HeaderValue::from_str(trace_id).map_err(|_| "invalid header")?;
    Ok(Response::builder().header("X-Upstream-Trace", header.to_str().unwrap_or_default()))
}

fn reject_crlf_before_header(Query(params): Query<HashMap<String, String>>) -> Result<ResponseBuilder, &'static str> {
    let reason = params.get("reason").cloned().unwrap_or_default();
    if reason.contains('\r') || reason.contains('\n') {
        return Err("invalid header");
    }

    Ok(Response::builder().header("X-Return-Reason", reason))
}
