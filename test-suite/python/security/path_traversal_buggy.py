from pathlib import Path

from django.http import FileResponse
from flask import request, send_file

UPLOAD_ROOT = Path("/srv/app/uploads")


def flask_download():
    name = request.args.get("file")
    return send_file(UPLOAD_ROOT / name)


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
