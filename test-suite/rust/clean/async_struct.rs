use std::time::Duration;

async fn fetch_once(id: u32) -> Result<String, Box<dyn std::error::Error>> {
    tokio::time::sleep(Duration::from_millis(50)).await;
    Ok(format!("{}", id))
}

async fn process(ids: Vec<u32>) -> Result<(), Box<dyn std::error::Error>> {
    let futures = ids.into_iter().map(fetch_once);
    for output in futures::future::try_join_all(futures).await? {
        println!("{}", output);
    }
    Ok(())
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let rt = tokio::runtime::Runtime::new()?;
    rt.block_on(process(vec![1,2,3]))?;
    Ok(())
}
