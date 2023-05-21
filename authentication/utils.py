"""
    Utility functions for authentication and profile related pages
    @package smartcook
    @author Noel Nagy
    @website: https://github.com/nagynooel
    ©2023 Noel Nagy - All rights reserved.
"""
import smtplib, os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from smartcook.settings import EMAIL_HOST, EMAIL_PORT,EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, EMAIL_FROM, BASE_DIR

from django.urls import reverse
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from .models import PasswordResetToken, DeactivateToken
from uuid import uuid4
import datetime

# Send a basic SMTP email using the parameters from the main settings file
# Items of the embeds list should be strings that contain the path from the smartcook directory
# E.g.: "authentication/static/authentication/img/email/Logo.png"
def send_smtp_email(recipient, subject, html_message, text_message, embeds=[]):
    smtp_server = EMAIL_HOST
    smtp_port = EMAIL_PORT
    
    smtp_user = EMAIL_HOST_USER
    smtp_password = EMAIL_HOST_PASSWORD
    
    from_email = EMAIL_FROM
    to_email = recipient

    with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
        server.login(smtp_user, smtp_password)

        msg = MIMEMultipart('alternative')

        # Add headers
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = "[SmartCook] " + subject

        # Attach multipart content
        msg.attach(MIMEText(text_message, 'plain'))
        msg.attach(MIMEText(html_message, 'html'))

        # Add logo to embeds
        embeds.append("authentication/static/authentication/img/email/Logo.png")

        # Attach embeds
        # CID is the lower case name of the file
        for embed in embeds:
            with open(os.path.join(BASE_DIR,embed), "rb") as f:
                img = MIMEImage(f.read())
                img.add_header("Content-ID", f"<{os.path.splitext(os.path.basename(f.name))[0].lower()}>")
            
            msg.attach(img)

        # send email
        server.send_message(msg, from_email, to_email)
    
    return True


# Send a password reset name to the given recipients email address
def send_password_reset_email(request, recipient):
    # Get user object
    try:
        user = User.objects.get(email=recipient)
    except User.DoesNotExist:
        raise ValueError("User does not exist")

    # Generate a token until it is unique
    token = uuid4()
    exists = True
    while exists:
        try:
            PasswordResetToken.objects.get(token = token)
            token = uuid4()
        except PasswordResetToken.DoesNotExist:
            exists = False

    # Set a expiry date of 30 minutes
    expiry = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=30)

    # Save the token
    PasswordResetToken.objects.create(user=user, token=token, expiry=expiry)

    # Create context
    context = {
        "first_name": user.first_name,
        "reset_link": "http://" + get_current_site(request).domain + reverse("reset_password", kwargs={'token':token}),
        "expiry_date": expiry
    }

    # Render the email content
    html = render_to_string("authentication/email/password_reset.html", context)
    text = render_to_string("authentication/email/password_reset.txt", context)

    # Send the reset email
    send_smtp_email(user.email, "Reset Your Password", html, text)

    return True


# Send an email that contains a link to deactivate the account
def send_deactivate_account_email(request, recipient):
    # Get user object
    try:
        user = User.objects.get(email=recipient)
    except User.DoesNotExist:
        raise ValueError("User does not exist")
    
    # Generate a token until it is unique
    token = uuid4()
    exists = True
    while exists:
        try:
            DeactivateToken.objects.get(token = token)
            token = uuid4()
        except DeactivateToken.DoesNotExist:
            exists = False
    
    # Set a expiry date of 30 minutes
    expiry = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=30)

    # Save the token
    DeactivateToken.objects.create(user=user, token=token, expiry=expiry)

    # Create context
    context = {
        "first_name": user.first_name,
        "deactivate_link": "http://" + get_current_site(request).domain + reverse("deactivate_account", kwargs={'token':token}),
        "expiry_date": expiry
    }

    # Render the email content
    html = render_to_string("authentication/email/deactivate_account.html", context)
    text = render_to_string("authentication/email/deactivate_account.txt", context)

    # Send the reset email
    send_smtp_email(user.email, "Reset Your Password", html, text)

    return True