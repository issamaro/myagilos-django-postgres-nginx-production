from email.message import EmailMessage
import smtplib

def sendemail(sender=None, password=None, receiver=None, subject=None, body=None):
    """
    Sends an email using the provided credentials and message details.

    Args:
        sender (str): The email address of the sender.
        password (str): The password for the sender's email account.
        receiver (str): The email address of the receiver.
        subject (str): The subject of the email.
        body (str): The body content of the email.

    Raises:
        ValueError: If any of the required arguments is missing.

    Returns:
        None
    """
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
    sendemail(sender="example@example.com", receiver="example@example.com", password="password123", subject="Test - Sending an email via Python", body="Hey, if you successfully received this email with no issue, then I am doing a good job.")
