#!/usr/bin/env python
import csv
import random
import string
import sys
import os
import traceback

sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ucbc.settings.dev")

from allauth.account.models import EmailAddress
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from django.core import mail
from django.contrib.sites.models import Site
from django.core.exceptions import ObjectDoesNotExist

#base_url = 'http://localhost:8000/'
CC = "admin@ucbc.org.nz"
enabled = True


def generate_password(email, first_name):
    s = ""
    for i in range(10):
        s += random.choice(string.ascii_lowercase)
    return s


def send_email(user, email_address, password):
    current_site = Site.objects.get_current()

    message = render_to_string(
        'account/email/email_confirmation_signup_message.txt', {
            'username': user.username,
            'password': password,
            'first_name': user.first_name,
            'current_site': current_site,
        })
    if enabled:
        mail.send_mail(
            'Welcome to the UC Brew Club Website',
            message,
            None,
            [email_address.email, CC],
            fail_silently=False)
    else:
        print(message)
        print("fake email sent to " + email_address.email + " with pw: " + password)


def create_user(first, last, email, password):
    username = first.lower() + last.lower()
    username = username.replace(" ", "")
    user = get_user_model().objects.create(
        username=username,
        first_name=first,
        last_name=last,
        email=email)
    user.set_password(password)
    user.save()
    print("New user: %s %s, u: %s e: %s, p: %s" % (first, last, username, email, password))
    return user


def create_email_address(user):
    return EmailAddress.objects.get_or_create(user=user, email=user.email, verified=True, primary=True)[0]


def create_and_email_user(first, last, email):
    try:
        password = generate_password(email, first_name=first)
        user = create_or_update_user(first, last, email, password)
        email_address = create_email_address(user)
        send_email(user, email_address, password)
    except Exception:
        print("Exception for user: %s, %s, %s" % (first, last, email))
        traceback.print_exc()


def create_or_update_user(first, last, email, password):
    try:
        user = get_user_model().objects.get(email=email)
        user.is_active = True
        user.save()
    except ObjectDoesNotExist:
        user = create_user(first, last, email, password)
    return user


def deactivate_old_users():
    print("deactivated %d users" % get_user_model().objects.filter(is_staff=False, is_active=True).update(is_active=False))


def main():
    deactivate_old_users()
    with open('brew_club_sign_2015.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for first, last, username, email in reader:
            create_and_email_user(first.strip(), last.strip(), email.strip())

if __name__ == "__main__":
    main()
