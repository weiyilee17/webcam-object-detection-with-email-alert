from os import getenv
from smtplib import SMTP
from email.message import EmailMessage

EMAIL_SENDER = getenv('EMAIL_SENDER')
EMAIL_RECEIVER = getenv('EMAIL_RECEIVER')
WEBCAM_APP_PASSWORD = getenv('WEBCAM_APP_PASSWORD')


def send_email(image_file_path):
    email_message = EmailMessage()

    email_message['Subject'] = 'New customer showed up! '
    email_message.set_content('We just detected a new customer.')

    with open(image_file_path, 'rb') as file:
        content = file.read()
        # subtype is for file extensions, what() from imghdr can figure it out, but is deprecated, so hard coded for now
        # Without subtype, the function fails to execute, but with the subtype alone doesn't make the file system
        # correctly recognize it as a png file. We would have to specifically add .png in the filename.
        email_message.add_attachment(
            content,
            maintype='image',
            subtype='png',
            filename=file.name
        )

    gmail_server = SMTP('smtp.gmail.com', 587)
    gmail_server.ehlo()
    gmail_server.starttls()
    gmail_server.login(EMAIL_SENDER, WEBCAM_APP_PASSWORD)
    gmail_server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, email_message.as_string())

    gmail_server.quit()


if __name__ == '__main__':
    send_email('images/image10.png')
