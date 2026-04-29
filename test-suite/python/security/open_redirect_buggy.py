from django.http import HttpResponseRedirect
from flask import redirect, request
from starlette.responses import RedirectResponse


def flask_login_redirect():
    next_url = request.args.get("next", "/")
    return redirect(next_url)


def flask_cookie_redirect():
    target = request.cookies.get("continue")
    return redirect(location=target)


def django_login_redirect(request):
    return HttpResponseRedirect(request.GET.get("next", "/"))


async def starlette_redirect(request):
    target = request.query_params.get("return_to", "/")
    return RedirectResponse(target)
