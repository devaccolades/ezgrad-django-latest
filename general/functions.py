from django.db.models import *
from random import randint
from django.contrib.auth.models import User

import random
import string
from django.core.mail import send_mail
from django.conf import settings



def generate_serializer_errors(args):
    message = ""
    for key, values in args.items():
        error_message = ""
        for value in values:
            error_message += value + ","
        error_message = error_message[:-1]

        # message += "%s : %s | " %(key,error_message)
        message += f"{key} - {error_message} | "
    return message[:-3]


def randomnumber(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1

    return randint(range_start, range_end)


def check_username(username):
    old_username = username
    if User.objects.filter(Q(username__icontains=username)).exists():
        print(username, "========old===========")
        sliced_phone = username[3:7]
        new_random_number = randomnumber(4)
        new_username = f'EZG{sliced_phone}{new_random_number}'
        print(new_username, "========new===========")
        check_username(new_username)
        return new_username
    else:
        return old_username
    
def generate_otp(length=6):
    characters = string.digits
    otp = ''.join(random.choice(characters) for _ in range(length))
    return otp

def send_otp_email(email, otp):
    subject = 'Your OTP for Login'
    message = f'Your OTP is: {otp}'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)


# from twilio.rest import Client
# def send_otp_phone(phone_number, otp):
#     account_sid = 'your_account_sid'  # Replace with your Twilio account SID
#     auth_token = 'your_auth_token'  # Replace with your Twilio auth token
#     twilio_phone_number = 'your_twilio_phone_number'  # Replace with your Twilio phone number

#     client = Client(account_sid, auth_token)
#     message = client.messages.create(
#         body=f'Your OTP is: {otp}',
#         from_=twilio_phone_number,
#         to=phone_number
#     )