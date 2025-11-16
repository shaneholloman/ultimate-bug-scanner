use std::sync::{Arc, Mutex};

fn compute(value: Option<i32>) -> Result<i32, &'static str> {
    value.ok_or("missing value")
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let shared = Arc::new(Mutex::new(0));
    let clone = Arc::clone(&shared);
    let handle = std::thread::spawn(move || {
        let mut guard = clone.lock().expect("lock poisoned");
        *guard += 1;
    });

    handle.join().expect("thread failed");
    let guard = shared.lock()?;
    println!("value: {}", *guard);
    println!("compute: {}", compute(Some(5))?);
    Ok(())
}
