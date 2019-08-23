from django.core.mail import EmailMessage


def sendMail(to, subject, message):
    msg = EmailMessage(subject, message, to=to)
    msg.content_subtype = 'html'
    try:
        msg.send()
    except Exception as e:
        pass