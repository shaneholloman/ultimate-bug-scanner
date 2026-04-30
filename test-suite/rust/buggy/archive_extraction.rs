use std::fs::{self, File};
use std::io::{self, Read};
use std::path::{Path, PathBuf};

fn extract_zip_member(mut member: zip::read::ZipFile<'_>, destination: &Path) -> io::Result<()> {
    let output_path = destination.join(member.name());
    if let Some(parent) = output_path.parent() {
        fs::create_dir_all(parent)?;
    }

    let mut output = File::create(&output_path)?;
    io::copy(&mut member, &mut output)?;
    Ok(())
}

fn extract_zip_member_via_variable(member: zip::read::ZipFile<'_>, destination: &Path) -> PathBuf {
    let archive_name = member.name();
    destination.join(archive_name)
}

fn extract_tar_entry<R: Read>(mut entry: tar::Entry<'_, R>, destination: &Path) -> io::Result<()> {
    let output_path = destination.join(entry.path()?);
    entry.unpack(output_path)?;
    Ok(())
}
