from django.core.mail import send_mail
from django.http import JsonResponse
from flask import jsonify, redirect, request, url_for


def django_password_reset_link(django_request, user):
    reset_url = django_request.build_absolute_uri(f"/reset/{user.token}")
    send_mail("Reset password", reset_url, "support@example.com", [user.email])


def django_get_host_link(django_request, token):
    host = django_request.get_host()
    verify_url = f"https://{host}/verify/{token}"
    return JsonResponse({"verify_url": verify_url})


def django_meta_host_link(django_request, token):
    host = django_request.META["HTTP_HOST"]
    return f"https://{host}/invite/{token}"


def flask_external_url_for():
    reset_url = url_for("reset_password", token=request.args["token"], _external=True)
    return jsonify(reset_url=reset_url)


def flask_host_url_callback():
    callback_url = request.host_url + "oauth/callback"
    return redirect(callback_url)


def flask_header_host_email(user):
    host = request.headers["Host"]
    link = "https://{}/confirm".format(host)
    send_mail("Confirm", link, "support@example.com", [user.email])


def flask_url_root_template():
    activation_link = f"{request.url_root}activate"
    return {"activation_link": activation_link}
