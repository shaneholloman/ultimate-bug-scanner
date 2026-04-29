import urllib.parse

from django.http import FileResponse, HttpResponse
from flask import Response, make_response, request, send_file
from werkzeug.utils import secure_filename


def sanitize_header_value(value):
    cleaned = str(value).replace("\r", "").replace("\n", "")
    if not cleaned:
        raise ValueError("empty header value")
    return cleaned


def flask_header_assignment_clean():
    response = make_response("ok")
    response.headers["X-Display-Name"] = sanitize_header_value(request.args["name"])
    return response


def django_header_assignment_clean(django_request):
    response = HttpResponse("ok")
    safe_filename = urllib.parse.quote(django_request.GET["filename"], safe="")
    response["Content-Disposition"] = f'attachment; filename="{safe_filename}"'
    return response


def response_headers_dict_clean():
    return Response("ok", headers={"X-Trace": "internal"})


def response_headers_variable_clean():
    safe_headers = {"X-Trace": urllib.parse.quote(request.args["trace"], safe="")}
    return Response("ok", headers=safe_headers)


def local_headers_subscript_clean():
    headers = {}
    headers["X-Trace"] = urllib.parse.quote(request.args["trace"], safe="")
    return Response("ok", headers=headers)


def headers_add_method_clean():
    response = make_response("ok")
    token = urllib.parse.quote(request.headers["X-Trace"], safe="")
    response.headers.add("X-Trace", token)
    return response


def headers_update_method_clean():
    response = make_response("ok")
    response.headers.update({"X-Session": sanitize_header_value(request.args["session"])})
    return response


def flask_download_name_clean():
    safe_download_name = secure_filename(request.args["name"])
    return send_file("/srv/reports/monthly.pdf", as_attachment=True, download_name=safe_download_name)


def django_file_response_clean():
    return FileResponse(iter([b"report"]), as_attachment=True, filename="monthly.pdf")
