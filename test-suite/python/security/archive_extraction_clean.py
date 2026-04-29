import tarfile
import zipfile
from pathlib import Path


def safe_destination(base: Path, member_name: str) -> Path:
    target = (base / member_name).resolve()
    if not target.is_relative_to(base.resolve()):
        raise ValueError("archive member escapes destination")
    return target


def unpack_tar_safely(archive_path: str, destination: str) -> None:
    base = Path(destination).resolve()
    with tarfile.open(archive_path) as archive:
        for member in archive.getmembers():
            safe_destination(base, member.name)
            archive.extract(member, base)


def unpack_tar_with_data_filter(archive_path: str, destination: str) -> None:
    with tarfile.open(archive_path) as archive:
        archive.extractall(destination, filter="data")


def unpack_zip_safely(archive_path: str, destination: str) -> None:
    base = Path(destination).resolve()
    with zipfile.ZipFile(archive_path) as archive:
        for member in archive.infolist():
            safe_destination(base, member.filename)
            archive.extract(member, base)


def unpack_tar_selected_safely(archive_path: str, destination: str) -> None:
    base = Path(destination).resolve()
    with tarfile.open(archive_path) as archive:
        member = archive.getmembers()[0]
        safe_destination(base, member.name)
        archive.extract(member, base)


class ReportExtractor:
    def extract(self, report_name: str) -> str:
        return report_name.removesuffix(".zip")


def parse_report_name(extractor: ReportExtractor, report_name: str) -> str:
    return extractor.extract(report_name)
