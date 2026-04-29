from urllib.parse import urljoin

from django.conf import settings
from django.core.mail import send_mail
from django.http import JsonResponse
from flask import current_app, jsonify, redirect, request, url_for

PUBLIC_BASE_URL = "https://example.com"


def django_password_reset_link(user):
    reset_url = urljoin(settings.PUBLIC_BASE_URL, f"/reset/{user.token}")
    send_mail("Reset password", reset_url, "support@example.com", [user.email])


def django_configured_link(token):
    verify_url = f"{settings.SITE_URL}/verify/{token}"
    return JsonResponse({"verify_url": verify_url})


def helper_validates_host(django_request):
    validate_allowed_host(django_request.get_host())
    return {"host_ok": True}


def flask_external_path_only():
    reset_path = url_for("reset_password", token=request.args["token"])
    return jsonify(reset_path=reset_path)


def flask_public_base_url_callback():
    callback_url = urljoin(current_app.config["PUBLIC_BASE_URL"], "oauth/callback")
    return redirect(callback_url)


def configured_constant_email(user):
    link = f"{PUBLIC_BASE_URL}/confirm"
    send_mail("Confirm", link, "support@example.com", [user.email])


def request_host_used_only_for_allowlist_check():
    host = request.headers["Host"]
    if not is_allowed_host(host):
        raise ValueError("untrusted host")
    return {"host_ok": True}


def validate_allowed_host(host):
    if host not in {"example.com"}:
        raise ValueError("untrusted host")
    return host


def is_allowed_host(host):
    return host == "example.com"
