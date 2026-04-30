use std::env;
use std::fs::{self, File, OpenOptions};
use std::io;
use std::path::PathBuf;

pub fn write_report(user_id: &str, body: &[u8]) -> io::Result<PathBuf> {
    let path = env::temp_dir().join(format!("ubs-report-{user_id}.json"));
    fs::write(&path, body)?;
    Ok(path)
}

pub fn create_fixed_cache(name: &str) -> io::Result<File> {
    let target = std::env::temp_dir().join(format!("cache-{name}.tmp"));
    File::create(&target)
}

pub fn create_direct_tmp(name: &str) -> io::Result<File> {
    std::fs::File::create(std::env::temp_dir().join(format!("direct-{name}.tmp")))
}

pub fn append_predictable_log(job: &str) -> io::Result<File> {
    let mut path = std::env::temp_dir();
    path.push(format!("job-{job}.log"));
    OpenOptions::new()
        .create(true)
        .write(true)
        .truncate(true)
        .open(&path)
}
