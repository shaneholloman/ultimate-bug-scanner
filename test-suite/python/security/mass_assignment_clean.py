from flask import request


class User:
    pass


ALLOWED_FIELDS = {"name", "email"}


def filtered_payload():
    raw = request.get_json()
    return {key: raw[key] for key in ALLOWED_FIELDS if key in raw}


def create_user():
    payload = filtered_payload()
    return User(name=payload["name"], email=payload["email"])


def update_profile(profile):
    data = request.form
    profile.name = data["name"]
    profile.email = data["email"]


def loop_setattr(user):
    data = request.form
    for field in ALLOWED_FIELDS:
        if field in data:
            setattr(user, field, data[field])


def django_create(request):
    return User(name=request.POST["name"], email=request.POST["email"])
