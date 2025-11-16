async fn fetch_data() -> Result<String, reqwest::Error> {
    reqwest::get("https://example.com").await?.text().await
}

async fn run() {
    let body = fetch_data().await;
    println!("{:?}", body);
    let handle = tokio::spawn(async move {
        fetch_data().await.unwrap();
    });
    println!("spawned: {:?}", handle);
}

fn main() {
    let _ = run();
}
