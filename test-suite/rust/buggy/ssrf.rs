use std::collections::HashMap;

use axum::extract::Query;
use reqwest::Client;

struct HeaderMap;
struct HeaderValue;
struct Request;

impl Request {
    fn headers(&self) -> HeaderMap {
        HeaderMap
    }

    fn query_string(&self) -> &str {
        "target=https://metadata.internal/latest"
    }
}

impl HeaderMap {
    fn get(&self, _name: &str) -> Option<HeaderValue> {
        Some(HeaderValue)
    }
}

impl HeaderValue {
    fn to_str(&self) -> Result<&str, ()> {
        Ok("https://metadata.internal/latest")
    }
}

async fn fetch_from_query(Query(params): Query<HashMap<String, String>>) -> Result<String, reqwest::Error> {
    let target = params.get("target_url").cloned().unwrap_or_default();
    reqwest::get(&target).await?.text().await
}

async fn fetch_from_header(client: &Client, req: Request) -> Result<(), reqwest::Error> {
    let callback = req.headers().get("x-callback-url").unwrap().to_str().unwrap();
    client.get(callback).send().await?;
    Ok(())
}

fn fetch_from_env() {
    let webhook = std::env::var("WEBHOOK_URL").unwrap();
    let _ = ureq::get(&webhook).call();
}

fn build_proxy_request() {
    let uri = std::env::args().nth(1).unwrap();
    let _ = http::Request::builder().uri(uri).body(());
}
