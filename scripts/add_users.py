#!/usr/bin/env python
import random
import sys
import os
from urllib.parse import urljoin

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ucbc.settings.dev")

from allauth.account.models import EmailConfirmation
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.core import mail
from django.contrib.sites.models import Site
from requests import Session
from pyquery import PyQuery as pq
import hashlib

base_url = 'http://localhost:8000/'


def generate_password(email, first_name):
    key = email + first_name
    full_hash = hashlib.sha1(key.encode("UTF-8")).hexdigest()
    return "".join([random.choice(full_hash) for i in range(10)])
    # return "".join([c for i, c in enumerate(full_hash) if i % 2 == 0])


def send_email(email, template_name, password, first_name, username):

    current_site = Site.objects.get_current()
    email_address = EmailConfirmation.objects.get(email_address__email=email)
    activate_url = reverse("account_confirm_email", args=[email_address.key])
    activate_url = urljoin(base_url, activate_url)

    message = render_to_string('account/email/email_confirmation_signup_message.txt',
                              {'username': username, 'password': password, 'activate_url': activate_url,
                               'current_site': current_site, })

    mail.send_mail(
        'Welcome to the UC Brew Club',
        message,
        None,
        [email],
        fail_silently=False)


def main():

    signup_url = urljoin(base_url, '/accounts/signup/')
    s = Session()

    def create_user(first_name, last_name, email):
        print("creating user %s %s, email: %s" % (first_name, last_name, email))
        if not first_name or not last_name or not email:
            raise ValueError()
        response = s.get(signup_url)
        d = pq(response.text)
        csrf = d("[name='csrfmiddlewaretoken']")[0].value
        password = generate_password(email, first_name)
        username = first_name.lower() + last_name.lower()
        username = username.replace(" ", "")
        response = s.post(signup_url, data={
            'csrfmiddlewaretoken': csrf,
            'username': username,
            'email': email,
            'password1': password,
            'password2': password,
            'confirmation_key': '',
        })
        errors = pq(response.text)(".errorlist li")
        if len(errors) > 0:
            for error in errors:
                print(error.text)
        else:
            print("updating + notifying user")
            get_user_model().objects.filter(username=username).update(first_name=first_name, last_name=last_name)
            send_email(
                email=email,
                template_name='account/email/email_confirmation_signup_message.txt',
                first_name=first_name,
                password=password,
                username=username)
        print("----------")

    create_user("oliver", "drake", "admin@ucbc.org.nz")


if __name__ == "__main__":
    # sys.path.append('c:\\my_projec_src_folder')
    main()
    # print(generate_password("o@d.drake.ch"))
