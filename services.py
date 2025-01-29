import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# Email configuration (Replace with environment variables or a config file)
FROM_EMAIL = "your_email@example.com"  # Replace with your email
EMAIL_PASSWORD = "your_app_password"  # Use an App Password if using Gmail with 2FA
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

def send_email(to_emails, subject, message):
    msg = MIMEMultipart()
    msg['From'] = FROM_EMAIL
    msg['To'] = ", ".join(to_emails)
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(FROM_EMAIL, EMAIL_PASSWORD)
        server.sendmail(FROM_EMAIL, to_emails, msg.as_string())
        server.quit()
        print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")

def notify_registration_with_code(full_name, payment):
    subject = "Client Registered with Code"
    commission = payment * 0.20
    message = (
        f"Hello Elyes,\n\n"
        f"A new client \"{full_name}\" has been registered using your code. "
        f"You'll receive a commission of {commission} DT."
    )
    send_email(["your_marketing_agent@example.com"], subject, message)

def notify_client_saved():
    subject = "New Client Registered"
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = f"A new client was saved on {current_time}."
    send_email(["youssef.harizi2005@gmail.com", "youssef.timoumi@esprit.tn"], subject, message)
