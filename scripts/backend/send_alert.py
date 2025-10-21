from twilio.rest import Client
import smtplib
import threading

# Twilio Configuration
TWILIO_SID = "AC3605484f3b77291bcf781321b17dc08b"
TWILIO_AUTH_TOKEN = "4e930a2225209b72769d765f25396ef0"
TWILIO_PHONE_NUMBER = "+13512081418"
OWNER_PHONE_NUMBER = "+919573911567"

# Email Configuration
EMAIL_SENDER = "sudhakarri567@gmail.com"
EMAIL_PASSWORD = "avam czjf kwcy nfvp"
EMAIL_RECEIVER = "sudhakarri597@gmail.com"

def send_sms():
    try:
        client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body="🚨 ALERT! An intruder has been detected.",
            from_=TWILIO_PHONE_NUMBER,
            to=OWNER_PHONE_NUMBER
        )
        print("✅ SMS Sent!")
    except Exception as e:
        print("❌ SMS Failed:", e)

def send_email(image_path):
    try:
        import email, ssl
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        from email.mime.base import MIMEBase
        from email import encoders

        # Setup email
        msg = MIMEMultipart()
        msg["From"] = EMAIL_SENDER
        msg["To"] = EMAIL_RECEIVER
        msg["Subject"] = "🚨 Intruder Alert!"

        body = "An intruder has been detected. Attached is their image."
        msg.attach(MIMEText(body, "plain"))

        # Attach the image
        with open(image_path, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f"attachment; filename=intruder.jpg")
            msg.attach(part)

        # Send the email
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
        server.quit()
        
        print("✅ Email Sent!")
    except Exception as e:
        print("❌ Email Failed:", e)

def send_alert(image_path):
    """ Sends SMS & Email alerts using threading """
    threading.Thread(target=send_sms).start()
    threading.Thread(target=send_email, args=(image_path,)).start()
