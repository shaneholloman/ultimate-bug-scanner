const MAX_BODY_BYTES: usize = 1024 * 1024;

fn bounded_router() -> axum::Router {
    axum::Router::new().layer(axum::extract::DefaultBodyLimit::max(MAX_BODY_BYTES))
}

async fn read_axum_body(body: axum::body::Body) -> Result<bytes::Bytes, axum::Error> {
    axum::body::to_bytes(body, MAX_BODY_BYTES).await
}

async fn collect_limited_body<B>(body: B) -> Result<bytes::Bytes, B::Error>
where
    B: http_body::Body<Data = bytes::Bytes> + Unpin,
{
    let limited = http_body_util::Limited::new(body, MAX_BODY_BYTES);
    Ok(limited.collect().await?.to_bytes())
}
