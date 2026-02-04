import time
from selenium.webdriver import Chrome
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from email_notification import EmailNotifier
from config import AppConfig
from logger import get_logger
from sys import platform
from daftlistings import Listing
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

log = get_logger(__name__)


# Selenium Send Automted Response


def get_driver() -> Chrome:
    # linux
    if platform == "linux" or platform == "linux2":
        driver_location = "./driver/chromedriver_linux"
        binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        service = Service(executable_path=driver_location)
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920x1024")
        options.binary_location = binary_location
        return webdriver.Chrome(service=service, options=options)
    elif platform == "darwin":
        driver_location = "./driver/chromedriver_mac_arm64"
        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")
        # options.add_argument('--headless')
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920x1024")
        service = Service(executable_path=driver_location)
        return webdriver.Chrome(service=service, options=options)

    elif platform == "win32":
        driver_location = "./driver/chromedriver_win32.exe"
        return webdriver.Chrome(service=Service(executable_path=driver_location))

    else:
        raise RuntimeError(f"Unsupported platform: {platform}")


def send_automated_response(
    listings: list[Listing],
    cache: dict,
    use_cached_values: bool,
    config: AppConfig,
    email_notifier: EmailNotifier,
) -> None:
    if len(listings) == 0:
        return

    driver = get_driver()
    account = config.daft_account

    try:
        login_daft(driver, account.email, account.password)
    except Exception as e:
        log.error(f"Login failed, saving screenshot: {e}")
        driver.get_screenshot_as_file("stealth-uc.png")

    # SEND MESSAGE
    for l in listings:
        sleep_time = 1
        log.info(f"Processing listing: {l.daft_link}")
        try:
            time.sleep(sleep_time)
            driver.get(l.daft_link)
            # Mail the AGENT Button
            time.sleep(sleep_time)

            try:
                popup = driver.find_element(
                    By.CSS_SELECTOR, '[aria-label="Email Agent"]'
                ).click()
                # If the element is found, you can interact with it here

            except NoSuchElementException:
                popup = driver.find_element(
                    By.CSS_SELECTOR, '[aria-label="Email"]'
                ).click()

            time.sleep(sleep_time * 2)
            try:
                already_applied_text = driver.find_element(
                    By.CSS_SELECTOR, '[data-tracking-id="contact-form-enquired-panel"]'
                )
                continue
            except NoSuchElementException:
                pass

            first_name_field = driver.find_element(
                By.CSS_SELECTOR, '[aria-label="firstName"]'
            )
            last_name_field = driver.find_element(
                By.CSS_SELECTOR, '[aria-label="lastName"]'
            )
            phone_number_field = driver.find_element(
                By.CSS_SELECTOR, '[aria-label="phone"]'
            )
            email_field = driver.find_element(By.CSS_SELECTOR, '[aria-label="email"]')
            number_of_tenants = driver.find_element(
                By.CSS_SELECTOR, '[data-testid="adultTenants-increment-button"]'
            )
            daft_message_field = driver.find_element(By.ID, "message")
            submit_button = driver.find_element(
                By.CSS_SELECTOR,
                '[aria-label="Send"][type="submit"][data-testid="submit-button"]',
            )

            if use_cached_values == False:
                # FIRST NAME
                driver.execute_script("arguments[0].value = '';", first_name_field)
                time.sleep(sleep_time)
                first_name_field.send_keys(account.first_name)
                time.sleep(sleep_time)

                # LAST NAME
                driver.execute_script("arguments[0].value = '';", last_name_field)
                time.sleep(sleep_time)
                last_name_field.send_keys(account.last_name)
                time.sleep(sleep_time)

                # EMAIL
                time.sleep(sleep_time)
                driver.execute_script("arguments[0].value = '';", email_field)
                email_field.send_keys(account.email)
                time.sleep(sleep_time)

                # PHONE NUMBER - REMOVE - AND ADD

                driver.execute_script("arguments[0].value = '';", phone_number_field)
                phone_number_field.click()

                phone_number_field.send_keys(account.phone_number)
                time.sleep(sleep_time)

                # INCREASE TENANT BUTTON
                number_of_tenants.click()

                time.sleep(sleep_time)

                # DAFT MESSAGE
                driver.execute_script("arguments[0].value = '';", daft_message_field)
                daft_message_field.send_keys(account.message_text)
                time.sleep(5)

            # # EMAIL AGENT
            try:
                time.sleep(sleep_time)
                submit_button.click()
            except Exception as e:
                pass

            time.sleep(5)

            success_text = driver.find_element(
                By.CSS_SELECTOR,
                '[data-testid="alert-message"]',
            ).text

            if success_text == "Your enquiry has been sent":
                log.info("Message sent to agent successfully")
            else:
                log.warning(f"Unexpected response: {success_text}")
                email_notifier.error_notify(l)
                log.error("Failed to notify agent")

        except Exception as e:
            if l.daft_link in cache:
                cache.pop(l.daft_link)
            log.error(f"Error processing listing: {e}")
            email_notifier.error_notify(l)
            log.error("Error notifying agent")

    driver.close()


# Selenium UTILS


def login_daft(driver: Chrome, email: str, password: str) -> None:
    log.info("Navigating to login page")
    driver.get("https://daft.ie")

    time.sleep(1)

    # Accept Cookies Button
    driver.find_element(By.ID, "didomi-notice-agree-button").click()

    # Navigate to Sign in PAGE <Clicking button>
    driver.find_element(
        By.CSS_SELECTOR, '[data-testid="top-level-active-nav-link"]'
    ).click()

    log.debug("Clicked sign-in button")

    # Signin TO DAFT ACCOUNT
    driver.find_element(By.ID, "username").send_keys("")
    driver.find_element(By.ID, "username").send_keys(email)
    driver.find_element(By.ID, "password").send_keys(password)

    log.info("Entering DAFT.IE credentials")

    # Press SignIN Button
    driver.find_element(By.ID, "kc-form-buttons").click()

    log.info("Login submitted")
