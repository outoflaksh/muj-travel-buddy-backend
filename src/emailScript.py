import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def sendMail(msgContent,email_sender,email_password,email_reciever,email_subject,html=False):
    context = ssl.create_default_context()
    msg = MIMEMultipart('alternative')
    msg['From'] = email_sender
    msg['To'] = email_reciever if isinstance(email_reciever,str) else ', '.join(email_reciever)
    msg['Subject'] = email_subject
    if html:msg.attach(MIMEText(msgContent, 'html'))
    else: msg.attach(MIMEText(msgContent, 'plain'))
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, email_reciever, msg.as_string())
            return 0
    except smtplib.SMTPException as e:
        #print("Error, email not sent.")
        #print(e)
        return e

