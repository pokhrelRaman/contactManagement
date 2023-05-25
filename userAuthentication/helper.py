from django.core.mail import send_mail
import uuid

def send_forget_mail(email):
    token = str(uuid.uuid4())
    subject = 'Password Reset for ContactManagement '
    message = f'Click on link to reset your password '
