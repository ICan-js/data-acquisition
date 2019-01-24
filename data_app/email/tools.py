import email, smtplib, ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class GmailSender:

    def __init__(self, subject, body, sender_mail, receiver_mail, password):
        self.__subject = subject
        self.__body = body
        self.__senderMail = sender_mail
        self.__receiverMail = receiver_mail
        self.__password = password

    def sendAttachEmail(self, filename):
        """Method to send email with attach
        """

        message = MIMEMultipart()
        message["From"] = self.__senderMail
        message["To"] = self.__receiverMail
        message["Subject"] = self.__subject
        message["Bcc"] = self.__receiverMail

        message.attach(MIMEText(self.__body, "plain"))

        part = self.__openFilename(filename)
        encoders.encode_base64(part)

        part.add_header(
            "Content-Disposition",
            f"attachment; filename = {filename}",
        )

        message.attach(part)
        text = message.as_string()

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(self.__senderMail, self.__password)
            server.sendmail(self.__senderMail, self.__receiverMail, text)

    def __openFilename(self, filename):
        """Method to open a filename to send in email
        """

        with open(filename, "rb") as attach:
            f = MIMEBase("application", "octet-stream")
            f.set_payload(attach.read())

        return f
