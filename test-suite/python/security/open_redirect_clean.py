from urllib.parse import urlparse

from django.http import HttpResponseRedirect
from django.utils.http import url_has_allowed_host_and_scheme
from flask import redirect, request, url_for


def is_safe_redirect(target: str) -> bool:
    parsed = urlparse(target)
    return parsed.scheme in ("", "https") and parsed.netloc in ("", "example.com")


def safe_redirect_target(raw_target: str | None) -> str:
    if not raw_target:
        return url_for("dashboard")
    parsed = urlparse(raw_target)
    if parsed.scheme or parsed.netloc:
        return url_for("dashboard")
    return raw_target


def flask_login_redirect():
    next_url = request.args.get("next", "/")
    if not is_safe_redirect(next_url):
        next_url = url_for("dashboard")
    return redirect(next_url)


def flask_helper_redirect():
    return redirect(safe_redirect_target(request.args.get("next")))


def django_login_redirect(request):
    target = request.GET.get("next", "/")
    if not url_has_allowed_host_and_scheme(target, allowed_hosts={"example.com"}):
        target = "/"
    return HttpResponseRedirect(target)
