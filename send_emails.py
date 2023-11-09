import smtplib, ssl
import os
from email.mime.text import MIMEText

'''
This is modular code to use for sending an email with the msg_str variable holding the string of email text to send. It is configured to use secret env variables defined below. It can be used to send to at&t cell email-to-text number in the variables.
'''
#define the text to send and assign to msg_str variable
msg_str = 'test message: test message text just executed'
receiver_email = os.environ['user_phones_email']

def send_email(msg_str,send_to=receiver_email):
    port = 465  # For SSL
    #define env variables below in secrets before use
    smtp_server = os.environ['smtp_sender_server']
    sender_email = os.environ['sending_email_account']
    # receiver_email = os.environ['user_phones_email']
    sender_email_pw = os.environ['sending_email_pw']

    msg = MIMEText(msg_str)

    msg['Subject'] = 'Market update!'
    msg['From'] = sender_email
    msg['To'] = send_to

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:

      server.login(sender_email, sender_email_pw)
      server.sendmail(sender_email, [send_to], msg.as_string())
      print('mail successfully sent')

#uses send mail function to execute test email with msg_str text:

if __name__ == "__main__":
  send_email(msg_str)



