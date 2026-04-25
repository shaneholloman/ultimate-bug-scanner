#![allow(dead_code)]

use std::time::Duration;

fn sync_maintenance_job() {
    std::thread::sleep(Duration::from_millis(10));
    let _ = std::fs::read_to_string("config.toml");
    let handle = std::thread::spawn(|| 42);
    let _ = handle.join();
}

async fn async_timer_is_non_blocking() {
    tokio::time::sleep(Duration::from_millis(10)).await;
}

mod tokio {
    pub mod time {
        use std::time::Duration;

        pub async fn sleep(_duration: Duration) {}
    }
}
