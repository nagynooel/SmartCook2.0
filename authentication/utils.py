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