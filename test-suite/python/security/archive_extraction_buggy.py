import tarfile
import zipfile


def unpack_tar(archive_path: str, destination: str) -> None:
    with tarfile.open(archive_path) as archive:
        archive.extractall(destination)


def unpack_zip(archive_path: str, destination: str) -> None:
    with zipfile.ZipFile(archive_path) as archive:
        archive.extractall(destination)


def unpack_tar_direct(archive_path: str, destination: str) -> None:
    tarfile.open(archive_path).extractall(destination)


def unpack_tar_fully_trusted(archive_path: str, destination: str) -> None:
    with tarfile.open(archive_path) as archive:
        archive.extractall(destination, filter=tarfile.fully_trusted_filter)
