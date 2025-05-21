import os
import random
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes


def generate_otp(user):
    otp = str(random.randint(0, 9999)).zfill(4)
    user.otp = otp
    user.save(update_fields=['otp'])
    return user


def otp_verification_mail(user):
    try:
        send_mail(
            'Otp Verification',
            f'Your verification code: {user.otp}',
            'noreply@example.com',
            [user.email],
            fail_silently=False,
        )
    except Exception as e:
        print(e, '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>e')
    return user


def send_reset_password_mail(user):
    try:
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        reset_url = f"{os.environ.get('WEB_URL')}/v1/password_reset_confirm/{uidb64}/{token}/"
        print(uidb64)
        print(token)
        send_mail(
            'Password Reset',
            f'Use this link to reset your password: {reset_url}',
            'noreply@example.com',
            [user.email],
            fail_silently=False,
        )
    except Exception as e:
        print(e, '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>e')
    return user
