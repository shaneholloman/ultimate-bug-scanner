use std::collections::HashMap;

use axum::extract::Query;
use reqwest::Client;
use url::Url;

fn safe_outbound_url(raw: &str) -> Result<String, &'static str> {
    let parsed = Url::parse(raw).map_err(|_| "invalid url")?;
    if parsed.scheme() != "https" {
        return Err("blocked scheme");
    }
    let allowed_hosts = ["api.example.com", "hooks.example.com"];
    if !allowed_hosts.contains(&parsed.host_str().unwrap_or_default()) {
        return Err("blocked host");
    }
    Ok(parsed.into())
}

async fn fetch_from_query(Query(params): Query<HashMap<String, String>>) -> Result<(), reqwest::Error> {
    let target = safe_outbound_url(params.get("target_url").map(String::as_str).unwrap_or("https://api.example.com"))
        .unwrap_or_else(|_| "https://api.example.com".to_string());
    reqwest::get(target).await?;
    Ok(())
}

async fn fetch_from_header(client: &Client, raw_header: &str) -> Result<(), reqwest::Error> {
    let callback = safe_outbound_url(raw_header).unwrap_or_else(|_| "https://hooks.example.com".to_string());
    client.get(callback).send().await?;
    Ok(())
}

fn fetch_from_config() {
    if let Ok(webhook) = safe_outbound_url("https://hooks.example.com/deploy") {
        let _ = ureq::get(&webhook).call();
    }
}
