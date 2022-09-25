from email.message import EmailMessage
import os
import smtplib
import sys
from daftlistings import Listing


# Sends Mail to Users about listings
def notify(listings: list[Listing]):
    recipients = os.getenv('recipients').split(',')
    sender = os.getenv("sender_email")
    if len(listings) > 0:
        msg = get_message(listings, recipients, sender)

        try:
            server = smtplib.SMTP(
                os.getenv("email_server"), os.getenv("email_port"))
        except:
            print(
                "[E] Unable to connect to email server, please check os.getenv(")
            sys.exit(-1)
        # server.set_debuglevel(True)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(os.getenv("email_user"), os.getenv("email_password"))
        server.sendmail(sender, recipients, msg.as_string(unixfrom=True))
        server.quit()
        print("[*] Email Send.")

# Notify helper function


def get_message(listings: list[Listing], recipients: list[str], sender: str | None) -> EmailMessage:
    text = "%d new ad(s) found.\n" % (len(listings))
    for l in listings:
        text += "-----\n%s\n%s\n%s\n\nImages:\n" % (
            l.title, l.daft_link, l.price)
        text_image = ""
        try:
            for i in l.images:
                text_image += "\n%s\n" % (i["size720x480"]) if (
                    "size720x480" in i.keys()) else ""
        except Exception as e:
            print(e)

        text += text_image

    msg = EmailMessage()
    msg['From'] = "Daft Notification : <%s>" % sender
    msg['To'] = ", ".join(recipients)
    msg['Subject'] = os.getenv("email_subject")
    msg.set_content(text)
    return msg


# ERROR NOTIFY

def error_notify(listing: list[Listing]):
    recipients = os.getenv('recipients').split(',')
    sender = os.getenv("sender_email")
    msg = get_error_message(listing, recipients, sender)

    try:
        server = smtplib.SMTP(
            os.getenv("email_server"), os.getenv("email_port"))
    except:
        print(
            "[E] Unable to connect to email server, please check os.getenv(")
        sys.exit(-1)
    # server.set_debuglevel(True)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(os.getenv("email_user"), os.getenv("email_password"))
    server.sendmail(sender, recipients, msg.as_string(unixfrom=True))
    server.quit()
    print("[*] Email Send.")


def get_error_message(listing: Listing, recipients: list[str], sender: str | None) -> EmailMessage:
    text = "Unable to send automated message to agent"
    text += "-----\n%s\n%s\n%s\n" % (listing.title,
                                     listing.daft_link, listing.price)

    msg = EmailMessage()
    msg['From'] = "Daft Notification : <%s>" % sender
    msg['To'] = ", ".join(recipients)
    msg['Subject'] = "Unable To send Automated Message: "
    msg.set_content(text)
    return msg
