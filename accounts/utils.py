from django.core.mail import send_mail
from django.conf import settings



def send_otp_email(user, otp_code, purpose="Verification"):
    subject = f"Your OTP Code for {purpose}"
    message = f"Hi {user.first_name},\n\nYour OTP code is {otp_code}. It is valid for 10 minutes."
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
