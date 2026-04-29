from flask import request


class User:
    pass


class Account:
    @classmethod
    def create(cls, values):
        return cls()


def create_user():
    return User(**request.get_json())


def create_user_from_cached_payload():
    payload = request.json
    return User(**payload)


def update_profile(profile):
    profile.update(request.form)
    profile.from_dict(request.values.to_dict())


def loop_setattr(user):
    for field, value in request.form.items():
        setattr(user, field, value)


def django_create(request):
    return Account.objects.create(**request.POST.dict())


def pydantic_parse():
    return User.model_validate(request.get_json())


def unsafe_form(form, user):
    form.populate_obj(user)
