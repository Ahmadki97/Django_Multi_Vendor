from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from decouple import config


def detectUser(user):
    if user.role == 1:
        redirect_Url = 'vendorDashboard'
        return redirect_Url
    elif user.role == 2:
        redirect_Url = 'custDashboard'
        return redirect_Url
    elif user.role == None and user.is_superadmin:
        redirect_Url = '/admin'
        return redirect_Url
    

def sendVerificaionEmail(request, user, email_subject, email_template):
    from_email = config('DEFAULT_FORM_EMAIL')
    current_site = get_current_site(request)
    mail_subject = email_subject
    message = render_to_string(email_template, {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    })
    to_email = user.email
    mail = EmailMessage(subject=mail_subject, body=message, to=[to_email], from_email=from_email)
    mail.send()



