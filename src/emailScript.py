import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def sendMail(msgContent,email_sender,email_password,email_reciever):
    context = ssl.create_default_context()
    msg = MIMEMultipart('alternative')
    msg['From'] = email_sender
    msg['To'] = email_reciever
    msg['Subject'] = 'Welcome to MUJ Travel Buddy!'
    msg.attach(MIMEText(msgContent, 'html'))
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.send_message(msg)
    except smtplib.SMTPException as e:
        print("Error, email not sent.")
        print(e)


