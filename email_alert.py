import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging

logger = logging.getLogger('TokyoTrainAlert')

class EmailAlert:
    def __init__(self, smtp_server, port, sender, password, recipient):
        self.smtp_server = smtp_server
        self.port = port
        self.sender = sender
        self.password = password
        self.recipient = recipient

    def send(self, subject, body):
        """Send an email with the given subject and body."""
        try:
            msg = MIMEMultipart()
            msg['From'] = self.sender
            msg['To'] = self.recipient
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))

            with smtplib.SMTP(self.smtp_server, self.port) as server:
                server.starttls()
                server.login(self.sender, self.password)
                server.send_message(msg)

            logger.info(f"Email alert sent: {subject}")
            return True
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            return False