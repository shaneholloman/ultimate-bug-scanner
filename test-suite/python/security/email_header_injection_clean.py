from django.core.mail import EmailMessage, EmailMultiAlternatives, send_mail
from email.message import EmailMessage as StdlibEmailMessage
from flask import request
from flask_mail import Message


def sanitize_email_header(value):
    cleaned = str(value).replace("\r", "").replace("\n", "")
    if not cleaned:
        raise ValueError("empty email header")
    return cleaned


def validate_email_address(value):
    address = sanitize_email_header(value)
    if "@" not in address:
        raise ValueError("invalid email address")
    return address


def django_send_mail_subject_clean():
    subject = sanitize_email_header(request.args["name"])
    return send_mail(subject, "body", "noreply@example.com", ["ops@example.com"])


def django_send_mail_recipient_clean(django_request):
    recipient = validate_email_address(django_request.GET["email"])
    return send_mail("Welcome", "body", "noreply@example.com", [recipient])


def django_email_message_from_clean(django_request):
    sender = validate_email_address(django_request.POST["sender"])
    return EmailMessage("Notice", "body", sender, ["ops@example.com"])


def django_email_message_headers_clean():
    headers = {"X-Trace": sanitize_email_header(request.headers["X-Trace"])}
    return EmailMessage("Notice", "body", "noreply@example.com", ["ops@example.com"], headers=headers)


def django_email_message_positional_headers_clean():
    trace = sanitize_email_header(request.args["trace"])
    return EmailMessage(
        "Notice",
        "body",
        "noreply@example.com",
        ["ops@example.com"],
        None,
        None,
        None,
        {"X-Trace": trace},
    )


def django_multi_alternatives_reply_to_clean():
    reply_to = validate_email_address(request.args["reply_to"])
    return EmailMultiAlternatives(
        "Notice",
        "body",
        "noreply@example.com",
        ["ops@example.com"],
        reply_to=[reply_to],
    )


def stdlib_header_assignment_clean():
    msg = StdlibEmailMessage()
    msg["Subject"] = sanitize_email_header(request.args["subject"])
    return msg


def stdlib_add_header_clean():
    msg = StdlibEmailMessage()
    msg.add_header("Reply-To", validate_email_address(request.args["reply_to"]))
    return msg


def flask_mail_message_clean():
    return Message(
        subject=sanitize_email_header(request.args["subject"]),
        sender="noreply@example.com",
        recipients=["ops@example.com"],
    )


def flask_mail_positional_recipient_clean():
    recipient = validate_email_address(request.args["recipient"])
    return Message("Notice", [recipient], sender="noreply@example.com")


def smtp_sendmail_clean(client):
    sender = validate_email_address(request.args["sender"])
    return client.sendmail(sender, ["ops@example.com"], "Subject: hi\n\nbody")


def smtp_send_message_envelope_clean(client, msg):
    sender = validate_email_address(request.args["sender"])
    return client.send_message(msg, from_addr=sender)
