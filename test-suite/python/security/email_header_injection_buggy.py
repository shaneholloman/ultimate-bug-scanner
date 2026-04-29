from django.core.mail import EmailMessage, EmailMultiAlternatives, send_mail
from email.message import EmailMessage as StdlibEmailMessage
from flask import request
from flask_mail import Message


def django_send_mail_subject():
    subject = f"Reset for {request.args['name']}"
    return send_mail(subject, "body", "noreply@example.com", ["ops@example.com"])


def django_send_mail_recipient(django_request):
    recipient = django_request.GET["email"]
    return send_mail("Welcome", "body", "noreply@example.com", [recipient])


def django_email_message_from(django_request):
    sender = django_request.POST["sender"]
    return EmailMessage("Notice", "body", sender, ["ops@example.com"])


def django_email_message_headers():
    headers = {"X-Trace": request.headers["X-Trace"]}
    return EmailMessage("Notice", "body", "noreply@example.com", ["ops@example.com"], headers=headers)


def django_email_message_positional_headers():
    trace = request.args["trace"]
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


def django_multi_alternatives_reply_to():
    reply_to = request.args["reply_to"]
    return EmailMultiAlternatives(
        "Notice",
        "body",
        "noreply@example.com",
        ["ops@example.com"],
        reply_to=[reply_to],
    )


def stdlib_header_assignment():
    msg = StdlibEmailMessage()
    msg["Subject"] = request.args["subject"]
    return msg


def stdlib_add_header():
    msg = StdlibEmailMessage()
    msg.add_header("Reply-To", request.args["reply_to"])
    return msg


def flask_mail_message():
    return Message(
        subject=request.args["subject"],
        sender="noreply@example.com",
        recipients=["ops@example.com"],
    )


def flask_mail_positional_recipient():
    return Message("Notice", [request.args["recipient"]], sender="noreply@example.com")


def smtp_sendmail(client):
    sender = request.args["sender"]
    return client.sendmail(sender, ["ops@example.com"], "Subject: hi\n\nbody")


def smtp_send_message_envelope(client, msg):
    return client.send_message(msg, from_addr=request.args["sender"])
