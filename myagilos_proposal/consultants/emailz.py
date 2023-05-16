from email.message import EmailMessage
import smtplib

def sendemail(sender=None, password=None, receiver=None, subject=None, body=None):
    if None in [sender, password, receiver, subject, body]:
        raise ValueError("Argument value is missing")
    else:
        msg = EmailMessage()
        msg["From"] = sender
        msg["To"] = receiver
        msg["Subject"] = subject
        msg.set_content(body)

        with smtplib.SMTP("smtp.office365.com", 587) as smtp:
            smtp.starttls()
            smtp.login(sender, password)
            smtp.send_message(msg)
if __name__ == "__main__":
    sendemail(sender="aca@agilos.com", receiver="aca@agilos.com", password="Agilos123", subject="Test - Sending an email via Python", body="Hey, if you successfully received this email with no issue, then I am doing a good job.")
