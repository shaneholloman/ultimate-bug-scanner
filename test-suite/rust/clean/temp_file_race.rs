use std::fs::{File, OpenOptions};
use std::io;
use std::path::Path;

pub fn write_named_temp(body: &[u8]) -> io::Result<tempfile::NamedTempFile> {
    let mut file = tempfile::NamedTempFile::new()?;
    std::io::Write::write_all(&mut file, body)?;
    Ok(file)
}

pub fn create_unique_with_builder(body: &[u8]) -> io::Result<tempfile::NamedTempFile> {
    let mut file = tempfile::Builder::new()
        .prefix("ubs-report-")
        .suffix(".json")
        .tempfile()?;
    std::io::Write::write_all(&mut file, body)?;
    Ok(file)
}

pub fn create_noclobber(path: &Path) -> io::Result<File> {
    OpenOptions::new()
        .write(true)
        .create_new(true)
        .open(path)
}

pub fn create_noclobber_in_temp(name: &str) -> io::Result<File> {
    let path = std::env::temp_dir().join(format!("safe-{name}.tmp"));
    OpenOptions::new()
        .write(true)
        .create_new(true)
        .open(&path)
}
