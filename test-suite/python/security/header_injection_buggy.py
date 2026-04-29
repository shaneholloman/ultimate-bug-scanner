from django.http import FileResponse, HttpResponse
from flask import Response, make_response, request, send_file


def flask_header_assignment():
    response = make_response("ok")
    response.headers["X-Display-Name"] = request.args["name"]
    return response


def django_header_assignment(django_request):
    response = HttpResponse("ok")
    filename = django_request.GET["filename"]
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    return response


def response_headers_dict():
    trace = request.headers["X-Trace"]
    return Response("ok", headers={"X-Trace": trace})


def response_headers_variable():
    headers = {"X-Trace": request.args["trace"]}
    return Response("ok", headers=headers)


def local_headers_subscript():
    headers = {}
    headers["X-Trace"] = request.args["trace"]
    return Response("ok", headers=headers)


def headers_add_method():
    response = make_response("ok")
    filename = request.form["filename"]
    response.headers.add("Content-Disposition", f'attachment; filename="{filename}"')
    return response


def headers_update_method():
    response = make_response("ok")
    response.headers.update({"X-Session": request.args["session"]})
    return response


def flask_download_name():
    return send_file("/srv/reports/monthly.pdf", as_attachment=True, download_name=request.args["name"])


def django_file_response(django_request):
    filename = django_request.GET["name"]
    return FileResponse(iter([b"report"]), as_attachment=True, filename=filename)
