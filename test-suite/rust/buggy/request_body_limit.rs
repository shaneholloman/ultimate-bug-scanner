async fn read_hyper_request(req: hyper::Request<hyper::Body>) -> Result<bytes::Bytes, hyper::Error> {
    let body = hyper::body::to_bytes(req.into_body()).await?;
    Ok(body)
}

async fn read_axum_body(body: axum::body::Body) -> bytes::Bytes {
    axum::body::to_bytes(body, usize::MAX).await.unwrap()
}

async fn collect_http_body(body: http_body_util::combinators::BoxBody<bytes::Bytes, hyper::Error>) -> bytes::Bytes {
    body.collect().await.unwrap().to_bytes()
}
