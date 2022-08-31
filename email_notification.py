from email.message import EmailMessage
import os
import smtplib
import sys


# Sends Mail to Users about listings
def notify(listings):
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


def get_message(listings, recipients, sender):
    text = "%d new ad(s) found.\n" % (len(listings))
    for i in listings:
        text += "-----\n%s\n%s\n%s\n" % (i.title, i.daft_link, i.price)

    msg = EmailMessage()
    msg['From'] = "Daft Notification : <%s>" % sender
    msg['To'] = ", ".join(recipients)
    msg['Subject'] = os.getenv("email_subject")
    msg.set_content(text)
    return msg


# ERROR NOTIFY

def error_notify(listing):
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


def get_error_message(listing, recipients, sender):
    text = "Unable to send automated message to agent"
    text += "-----\n%s\n%s\n%s\n" % (listing.title,
                                     listing.daft_link, listing.price)

    msg = EmailMessage()
    msg['From'] = "Daft Notification : <%s>" % sender
    msg['To'] = ", ".join(recipients)
    msg['Subject'] = "Unable To send Automated Message: "
    msg.set_content(text)
    return msg
