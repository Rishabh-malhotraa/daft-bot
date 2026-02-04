"""
Selenium automation for applying to Daft.ie listings.

Usage:
    bot = DaftBot(config, email_notifier, headless=True)
    bot.process_listings(listings, cache, use_cached_values=True)
"""

import time
from pathlib import Path
from datetime import datetime
from typing import TYPE_CHECKING

from selenium.webdriver import Chrome
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    WebDriverException,
)

from webdriver_manager.chrome import ChromeDriverManager

if TYPE_CHECKING:
    from daftlistings import Listing

from .email_notification import EmailNotifier
from .config import AppConfig
from .logger import get_logger

log = get_logger(__name__)



class DaftLoginError(Exception):
    """Raised when login to Daft.ie fails."""
    pass


class DaftSubmissionError(Exception):
    """Raised when form submission fails."""
    pass

class DaftBot:
    """
    Automated bot for applying to Daft.ie rental listings.

    Usage:
        bot = DaftBot(config, email_notifier, headless=True)
        bot.process_listings(listings, cache, use_cached_values=True)

    The bot handles:
        - Browser setup and cleanup
        - Login to Daft.ie
        - Applying to each listing
        - Error handling and screenshots
        - Email notifications on failure
    """

    DEFAULT_TIMEOUT = 10  # seconds

    # Centralized selectors - easy to update when Daft changes their UI
    SELECTORS = {
        "cookie_accept": "#didomi-notice-agree-button",
        "sign_in_link": '[data-testid="top-level-active-nav-link"]',
        "username": "#username",
        "password": "#password",
        "login_submit": "#kc-form-buttons",
        "email_agent": '[aria-label="Email Agent"]',
        "email_fallback": '[aria-label="Email"]',
        "already_applied": '[data-tracking-id="contact-form-enquired-panel"]',
        "first_name": '[aria-label="firstName"]',
        "last_name": '[aria-label="lastName"]',
        "phone": '[aria-label="phone"]',
        "email": '[aria-label="email"]',
        "tenants_increment": '[data-testid="adultTenants-increment-button"]',
        "message": "#message",
        "submit_button": '[data-testid="submit-button"][type="submit"]',
        "success_message": '[data-testid="alert-message"]',
        "feedback_close": "#wootric-close",
    }

    def __init__(
        self,
        config: AppConfig,
        email_notifier: EmailNotifier,
        headless: bool = True,
    ) -> None:
        """
        Initialize the DaftBot.

        Args:
            config: Application configuration with account details.
            email_notifier: Email notifier for error notifications.
            headless: If True, run browser without visible window (for servers).
                      If False, show browser window (for local testing).
        """
        self.config = config
        self.email_notifier = email_notifier
        self.headless = headless
        self._driver: Chrome | None = None

    def process_listings(
        self,
        listings: list["Listing"],
        cache: dict,
        use_cached_values: bool = True,
    ) -> None:
        """
        Process all listings: login once, then apply to each.

        Args:
            listings: List of Daft listings to apply to.
            cache: Cache dict to track applied listings.
            use_cached_values: If True, use cached form values.
        """
        if not listings:
            log.info("No listings to process")
            return

        log.info(f"Processing {len(listings)} listings")

        try:
            self._start_driver()
            self._login()

            for listing in listings:
                self._process_single_listing(listing, cache, use_cached_values)
                time.sleep(2)  # Delay between listings to avoid rate limiting

        except DaftLoginError as e:
            log.error(f"Login failed: {e}")
            if listings:
                self.email_notifier.error_notify(listings[0])

        finally:
            self._stop_driver()

        log.info("Finished processing all listings")

    # =========================================================================
    # Driver Management
    # =========================================================================

    def _start_driver(self) -> None:
        """Start the Chrome WebDriver."""
        options = webdriver.ChromeOptions()

        # Common options for all platforms
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-infobars")

        # Reduce detection as a bot
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)

        if self.headless:
            options.add_argument("--headless=new")
            options.add_argument("--disable-gpu")
            options.add_argument("--remote-debugging-port=9222")
            log.info("Starting Chrome in headless mode")
        else:
            options.add_argument("--start-maximized")
            log.info("Starting Chrome in visible mode (for local testing)")

        service = Service(ChromeDriverManager().install())
        self._driver = webdriver.Chrome(service=service, options=options)
        self._driver.implicitly_wait(5)

    def _stop_driver(self) -> None:
        """Stop and clean up the WebDriver."""
        if self._driver:
            try:
                self._driver.quit()
                log.debug("Browser closed")
            except Exception as e:
                log.warning(f"Error closing driver: {e}")
            finally:
                self._driver = None

    @property
    def driver(self) -> Chrome:
        """Get the current driver, raising if not started."""
        if self._driver is None:
            raise RuntimeError("Driver not started. Call _start_driver() first.")
        return self._driver

    # =========================================================================
    # Core Flow
    # =========================================================================

    def _login(self) -> None:
        """
        Login to Daft.ie account.
        Raises DaftLoginError if login fails.
        """
        log.info("Navigating to Daft.ie for login")
        self.driver.get("https://daft.ie")

        # Accept cookies (may not always appear)
        if self._safe_click(self.SELECTORS["cookie_accept"], timeout=5):
            log.debug("Accepted cookies")

        self._dismiss_popups()

        # Navigate to sign in page
        if not self._safe_click(self.SELECTORS["sign_in_link"]):
            raise DaftLoginError("Could not find sign-in link")

        log.debug("Clicked sign-in button")
        time.sleep(1)

        # Fill credentials
        try:
            account = self.config.daft_account

            username_field = self._wait_for_element(self.SELECTORS["username"])
            username_field.clear()
            username_field.send_keys(account.email)

            password_field = self._wait_for_element(self.SELECTORS["password"])
            password_field.send_keys(account.password)

            log.info("Entering credentials")

            if not self._safe_click(self.SELECTORS["login_submit"]):
                raise DaftLoginError("Could not click login button")

            log.info("Login submitted, waiting for redirect...")
            time.sleep(3)

            if "login" in self.driver.current_url.lower():
                self._take_screenshot("login_failed")
                raise DaftLoginError("Login appears to have failed - still on login page")

            log.info("Login successful")

        except TimeoutException as e:
            self._take_screenshot("login_timeout")
            raise DaftLoginError(f"Timeout during login: {e}")

    def _process_single_listing(
        self,
        listing: "Listing",
        cache: dict,
        use_cached_values: bool,
    ) -> None:
        """Process a single listing with error handling."""
        try:
            success = self._apply_to_listing(listing, use_cached_values)

            if not success:
                self._handle_failure(listing, cache)

        except WebDriverException as e:
            log.error(f"WebDriver error for {listing.daft_link}: {e}")
            self._handle_failure(listing, cache)
            self._take_screenshot("webdriver_error")

        except Exception as e:
            log.error(f"Unexpected error for {listing.daft_link}: {e}")
            self._handle_failure(listing, cache)

    def _apply_to_listing(self, listing: "Listing", use_cached_values: bool) -> bool:
        """
        Apply to a single listing. Returns True if successful.
        """
        account = self.config.daft_account
        log.info(f"Processing listing: {listing.daft_link}")

        self.driver.get(listing.daft_link)
        time.sleep(2)
        self._dismiss_popups()

        # Click email agent button (try primary, then fallback)
        if not self._safe_click(self.SELECTORS["email_agent"], timeout=5):
            if not self._safe_click(self.SELECTORS["email_fallback"], timeout=5):
                log.warning("Could not find email agent button")
                self._take_screenshot("no_email_button")
                return False

        time.sleep(2)
        self._dismiss_popups()

        # Check if already applied
        try:
            self.driver.find_element(By.CSS_SELECTOR, self.SELECTORS["already_applied"])
            log.info("Already applied to this listing, skipping")
            return True
        except NoSuchElementException:
            pass

        # Fill form if not using cached values
        if not use_cached_values:
            try:
                self._fill_field("first_name", account.first_name)
                self._fill_field("last_name", account.last_name)
                self._fill_field("email", account.email)
                self._fill_field("phone", account.phone_number)

                self._safe_click(self.SELECTORS["tenants_increment"])

                self._fill_field("message", account.message_text)
                time.sleep(1)

            except TimeoutException as e:
                log.error(f"Timeout filling form: {e}")
                self._take_screenshot("form_timeout")
                return False

        # Submit
        self._dismiss_popups()
        if not self._safe_click(self.SELECTORS["submit_button"]):
            log.error("Could not click submit button")
            self._take_screenshot("submit_failed")
            return False

        time.sleep(3)

        # Verify success
        try:
            success_element = self._wait_for_element(
                self.SELECTORS["success_message"], timeout=10
            )
            success_text = success_element.text

            if "enquiry has been sent" in success_text.lower():
                log.info("Application submitted successfully")
                return True
            else:
                log.warning(f"Unexpected response: {success_text}")
                self._take_screenshot("unexpected_response")
                return False

        except TimeoutException:
            log.warning("Could not verify submission success")
            self._take_screenshot("no_success_message")
            return False

    def _handle_failure(self, listing: "Listing", cache: dict) -> None:
        """Handle a failed listing application."""
        if listing.daft_link in cache:
            cache.pop(listing.daft_link)
        self.email_notifier.error_notify(listing)

    # =========================================================================
    # Helper Methods
    # =========================================================================

    def _wait_for_element(
        self,
        selector: str,
        by: str = By.CSS_SELECTOR,
        timeout: int | None = None,
        clickable: bool = False,
    ):
        """Wait for an element to be present/clickable and return it."""
        timeout = timeout or self.DEFAULT_TIMEOUT
        condition = (
            EC.element_to_be_clickable((by, selector))
            if clickable
            else EC.presence_of_element_located((by, selector))
        )
        return WebDriverWait(self.driver, timeout).until(condition)

    def _safe_click(self, selector: str, timeout: int | None = None) -> bool:
        """Safely click an element, returning True if successful."""
        try:
            element = self._wait_for_element(selector, clickable=True, timeout=timeout)
            element.click()
            return True
        except (TimeoutException, NoSuchElementException) as e:
            log.debug(f"Could not click {selector}: {e}")
            return False

    def _dismiss_popups(self) -> None:
        """Dismiss any feedback/survey popups that might appear."""
        popup_selectors = [
            self.SELECTORS["feedback_close"],
            '[aria-label="Close"]',
            '[data-testid="close-button"]',
        ]
        for selector in popup_selectors:
            try:
                element = self.driver.find_element(By.CSS_SELECTOR, selector)
                element.click()
                log.debug(f"Dismissed popup: {selector}")
                time.sleep(0.5)
            except NoSuchElementException:
                pass

    def _fill_field(self, field_name: str, value: str) -> None:
        """Clear and fill a form field by name."""
        selector = self.SELECTORS.get(field_name)
        if not selector:
            raise ValueError(f"Unknown field: {field_name}")

        log.debug(f"Filling field: {field_name}")
        try:
            element = self._wait_for_element(selector)
            self.driver.execute_script("arguments[0].value = '';", element)
            time.sleep(0.3)
            element.send_keys(value)
            log.debug(f"Filled field: {field_name}")
        except TimeoutException:
            log.error(f"Timeout waiting for field: {field_name}")
            raise
        except Exception as e:
            log.error(f"Error filling field '{field_name}': {e}")
            raise

    def _take_screenshot(self, name: str) -> str:
        """Take a screenshot with timestamp for debugging."""
        screenshots_dir = Path("screenshots")
        screenshots_dir.mkdir(exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = screenshots_dir / f"{name}_{timestamp}.png"
        self.driver.get_screenshot_as_file(str(filename))
        log.info(f"Screenshot saved: {filename}")
        return str(filename)
