#![allow(dead_code)]

use std::time::Duration;

async fn blocks_executor() {
    std::thread::sleep(Duration::from_millis(10));
    let _ = std::fs::read_to_string("config.toml");
    let _ = futures::executor::block_on(async { 7 });
    std::thread::spawn(|| expensive_cpu_work());
}

fn expensive_cpu_work() -> usize {
    42
}
