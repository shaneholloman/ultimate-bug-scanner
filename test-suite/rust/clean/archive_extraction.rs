use std::fs::{self, File};
use std::io::{self, Read};
use std::path::{Path, PathBuf};

fn extract_zip_member(mut member: zip::read::ZipFile<'_>, destination: &Path) -> io::Result<()> {
    let safe_child = match member.enclosed_name() {
        Some(name) => name.to_owned(),
        None => return Ok(()),
    };
    let output_path = destination.join(safe_child);
    if let Some(parent) = output_path.parent() {
        fs::create_dir_all(parent)?;
    }

    let mut output = File::create(&output_path)?;
    io::copy(&mut member, &mut output)?;
    Ok(())
}

fn checked_destination(destination: &Path, safe_child: &Path) -> io::Result<PathBuf> {
    let base = destination.canonicalize()?;
    let candidate = base.join(safe_child);
    let parent = candidate.parent().unwrap_or(&base);
    fs::create_dir_all(parent)?;
    let parent = parent.canonicalize()?;
    if !parent.starts_with(&base) {
        return Err(io::Error::new(io::ErrorKind::PermissionDenied, "archive path escaped"));
    }
    Ok(candidate)
}

fn extract_tar_entry<R: Read>(mut entry: tar::Entry<'_, R>, destination: &Path) -> io::Result<()> {
    entry.unpack_in(destination)?;
    Ok(())
}
