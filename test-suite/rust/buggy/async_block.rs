use std::time::Duration;

async fn slow_fetch() -> Result<String, ()> {
    tokio::time::sleep(Duration::from_secs(5)).await;
    Ok("data".to_string())
}

async fn process(ids: Vec<u32>) {
    let mut handles = Vec::new();
    for id in ids {
        // BUG: spawn blocking + unwrap inside async
        handles.push(tokio::spawn(async move {
            let data = slow_fetch().await.unwrap();
            println!("{} {}", id, data);
        }));
    }
    for h in handles {
        h.await.unwrap();
    }
}

fn main() {
    let rt = tokio::runtime::Runtime::new().unwrap();
    rt.block_on(process(vec![1, 2, 3]));
}
