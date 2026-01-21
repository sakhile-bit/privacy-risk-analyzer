import smtplib
from email.mime.text import MIMEText

def send_email_alert(subject, body, to_email, smtp_server, smtp_port, smtp_user, smtp_pass):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = smtp_user
    msg['To'] = to_email
    with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
        server.login(smtp_user, smtp_pass)
        server.sendmail(smtp_user, [to_email], msg.as_string())
