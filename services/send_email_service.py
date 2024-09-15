import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import config
from dotenv import load_dotenv
import os
from templates.html_template import body_template


load_dotenv()

def send_email(to_address, code):
    server = None
    try:
        sender_email = os.getenv('EMAIL_SENDER')
        receiver_email = to_address
        password = os.getenv('EMAIL_SENDER_PASSWORD')

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = config.EMAIL_SETTINGS['email_subject']

        body = body_template.format(code=code)
        msg.attach(MIMEText(body, 'html'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
        print("Email sent successfully.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if server:
            server.set_debuglevel(1)
            server.quit()
