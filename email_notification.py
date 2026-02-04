from email.message import EmailMessage
import smtplib
import sys
from daftlistings import Listing
from config import EmailConfig
from logger import get_logger

log = get_logger(__name__)


class EmailNotifier:
    """Handles email notifications for Daft listings."""

    def __init__(self, config: EmailConfig):
        """Initialize EmailNotifier with configuration."""
        self.config = config

    def notify(self, listings: list[Listing]) -> None:
        """Send notification email about new listings."""
        if len(listings) > 0:
            msg = self._build_listings_message(listings)
            self._send_email(msg)

    def error_notify(self, listing: Listing) -> None:
        """Send notification email when automated message fails."""
        msg = self._build_error_message(listing)
        self._send_email(msg)

    def _create_smtp_connection(self) -> smtplib.SMTP:
        """Create and configure SMTP connection."""
        try:
            server = smtplib.SMTP(self.config.server, self.config.port)
        except ValueError as e:
            log.error(f"Configuration error: {e}")
            sys.exit(1)
        except Exception as e:
            log.error(f"Unable to connect to email server: {e}")
            sys.exit(1)

        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(self.config.user, self.config.password)
        return server

    def _send_email(self, msg: EmailMessage) -> None:
        """Send email using SMTP."""
        server = self._create_smtp_connection()
        try:
            server.sendmail(
                self.config.sender, self.config.recipients, msg.as_string(unixfrom=True)
            )
        finally:
            server.quit()
        log.info("Email sent successfully")

    def _build_listings_message(self, listings: list[Listing]) -> EmailMessage:
        """Build email message for listing notifications."""
        text = f"{len(listings)} new ad(s) found.\n"
        for listing in listings:
            text += f"-----\n{listing.title}\n{listing.daft_link}\n{listing.price}\n\nImages:\n"
            try:
                for img in listing.images:
                    if "size720x480" in img:
                        text += f"\n{img['size720x480']}\n"
            except Exception as e:
                log.warning(f"Error processing listing images: {e}")

        msg = EmailMessage()
        msg["From"] = f"Daft Notification : <{self.config.sender}>"
        msg["To"] = ", ".join(self.config.recipients)
        msg["Subject"] = self.config.subject
        msg.set_content(text)
        return msg

    def _build_error_message(self, listing: Listing) -> EmailMessage:
        """Build email message for error notifications."""
        text = "Unable to send automated message to agent\n"
        text += f"-----\n{listing.title}\n{listing.daft_link}\n{listing.price}\n"

        msg = EmailMessage()
        msg["From"] = f"Daft Notification : <{self.config.sender}>"
        msg["To"] = ", ".join(self.config.recipients)
        msg["Subject"] = "Unable To Send Automated Message"
        msg.set_content(text)
        return msg
