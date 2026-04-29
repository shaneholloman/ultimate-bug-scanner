from pathlib import Path

from django.http import FileResponse
from flask import request, send_file

UPLOAD_ROOT = Path("/srv/app/uploads")


def flask_download():
    name = request.args.get("file")
    return send_file(UPLOAD_ROOT / name)


def flask_upload_save():
    uploaded = request.files["avatar"]
    target = UPLOAD_ROOT / uploaded.filename
    uploaded.save(target)
    return {"saved": uploaded.filename}


def flask_upload_save_direct():
    request.files["report"].save(
        UPLOAD_ROOT / request.files["report"].filename
    )
    return {"saved": True}


def flask_upload_save_keyword():
    uploaded = request.files["invoice"]
    uploaded.save(dst=UPLOAD_ROOT / uploaded.filename)
    return {"saved": uploaded.filename}


def raw_open_download():
    target = request.values.get("path")
    return open(target, "rb").read()


def django_download(request):
    name = request.GET["document"]
    path = UPLOAD_ROOT / name
    return FileResponse(open(path, "rb"))


async def starlette_preview(request):
    filename = request.path_params["filename"]
    return (UPLOAD_ROOT / filename).read_text()
