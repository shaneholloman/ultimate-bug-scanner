from pathlib import Path

from flask import request, send_file
from werkzeug.utils import secure_filename

UPLOAD_ROOT = Path("/srv/app/uploads").resolve()


def validate_path(raw_name: str | None) -> Path:
    if not raw_name:
        raise ValueError("missing file")
    candidate = (UPLOAD_ROOT / raw_name).resolve()
    candidate.relative_to(UPLOAD_ROOT)
    return candidate


def flask_download():
    name = request.args.get("file")
    return send_file(validate_path(name))


def sanitized_filename_download():
    name = secure_filename(request.values.get("name", ""))
    target = UPLOAD_ROOT / name
    return target.read_bytes()


def sanitized_upload_save():
    uploaded = request.files["avatar"]
    name = secure_filename(uploaded.filename)
    target = UPLOAD_ROOT / name
    uploaded.save(target)
    return {"saved": name}


def containment_checked_upload_save():
    uploaded = request.files["document"]
    target = validate_path(uploaded.filename)
    uploaded.save(target)
    return {"saved": target.name}


def sanitized_upload_save_keyword():
    uploaded = request.files["invoice"]
    name = secure_filename(uploaded.filename)
    uploaded.save(dst=UPLOAD_ROOT / name)
    return {"saved": name}


def containment_checked_download():
    target = validate_path(request.args.get("document"))
    return target.read_bytes()
