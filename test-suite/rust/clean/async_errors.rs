async fn fetch_data() -> Result<String, reqwest::Error> {
    reqwest::get("https://example.com").await?.text().await
}

async fn run() -> Result<(), reqwest::Error> {
    match fetch_data().await {
        Ok(body) => println!("{}", body),
        Err(err) => {
            eprintln!("request failed: {err}");
            return Err(err);
        }
    }
    let handle = tokio::spawn(async move {
        if let Err(err) = fetch_data().await {
            eprintln!("background error: {err}");
        }
    });
    handle.await.ok();
    Ok(())
}

fn main() {
    let _ = run();
}
