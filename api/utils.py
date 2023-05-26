from django.core.mail import send_mail

def send_otp_email(email, otp):
    subject = 'OTP Verification'
    message = f'Your OTP for verification is: {otp}'
    from_email = 'mepillai98@gmail.com'  # Replace with your email address or a valid sender address
    recipient_list = [email]

    send_mail(subject, message, from_email, recipient_list)
