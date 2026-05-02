use axum::extract::Query;
use axum::response::Redirect;
use std::collections::HashMap;

const LOCATION: &str = "Location";

struct HeaderMap;
struct HeaderValue;
struct Request;
struct Response;
struct ResponseBuilder;
struct Uri;

impl HeaderMap {
    fn get(&self, _name: &str) -> Option<HeaderValue> {
        Some(HeaderValue)
    }
}

impl HeaderValue {
    fn to_str(&self) -> Result<&str, ()> {
        Ok("//evil.example/login")
    }
}

impl Request {
    fn headers(&self) -> HeaderMap {
        HeaderMap
    }

    fn uri(&self) -> Uri {
        Uri
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

impl Uri {
    fn host(&self) -> Option<&str> {
        Some("attacker.example")
    }
}

fn redirect_from_query(Query(params): Query<HashMap<String, String>>) -> Redirect {
    let target = params.get("next").cloned().unwrap_or_default();
    Redirect::to(&target)
}

fn redirect_from_header(req: Request) -> Redirect {
    let target = req
        .headers()
        .get("x-return-to")
        .and_then(|value| value.to_str().ok())
        .unwrap_or("/");
    Redirect::temporary(target)
}

fn redirect_location_header(req: Request) -> ResponseBuilder {
    let target = req
        .headers()
        .get("x-redirect-url")
        .and_then(|value| value.to_str().ok())
        .unwrap_or("/");
    Response::builder().header(LOCATION, target)
}

fn redirect_from_host(req: Request) -> Redirect {
    let target = format!("https://{}/dashboard", req.uri().host().unwrap_or_default());
    Redirect::permanent(&target)
}

fn validate_after_redirect(Query(params): Query<HashMap<String, String>>) -> Result<Redirect, &'static str> {
    let target = params.get("continue").cloned().unwrap_or_default();
    let response = Redirect::to(&target);
    if !(target.starts_with('/') && !target.starts_with("//")) {
        return Err("blocked redirect");
    }
    Ok(response)
}
