import os
import time
from selenium.webdriver import Chrome
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from email_notification import error_notify
from sys import platform
from daftlistings import Listing

# Selenium Send Automted Response


def get_driver() -> Chrome:
    # linux
    if platform == "linux" or platform == "linux2":
        driver_location = "./driver/chromedriver_linux"
        binary_location = "/usr/bin/google-chrome"

        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("window-size=1920x1024")
        options.binary_location = binary_location
        return webdriver.Chrome(executable_path=driver_location, chrome_options=options)
    elif platform == "darwin":
        driver_location = "./driver/chromedriver_mac_arm64"
        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("window-size=1920x1024")
        return webdriver.Chrome(executable_path=driver_location, chrome_options=options)

    elif platform == "win32":
        driver_location = "./driver/chromedriver_win32.exe"
        return webdriver.Chrome(executable_path=driver_location)


def send_automated_response(listings: list[Listing]):
    if len(listings) == 0:
        return

    driver = get_driver()

    login_daft(driver)

    # SEND MESSAGE
    for l in listings:
        print(l.daft_link)
        try:
            driver.get(l.daft_link)
            # Mail the AGENT Button
            time.sleep(1)
            driver.find_element(By.CLASS_NAME, "cWKcCS").click()
            time.sleep(1)
            driver.find_element(By.ID, "keyword1").send_keys(
                os.getenv('daft_name'))
            time.sleep(1)
            driver.find_element(By.ID, "keyword2").send_keys(
                os.getenv("daft_email"))
            time.sleep(1)
            driver.find_element(By.ID, "keyword3").send_keys(
                os.getenv("daft_phone_number"))
            time.sleep(1)
            driver.find_element(By.ID, "message").send_keys(
                os.getenv("daft_text"))


            time.sleep(5)

            driver.find_element(
                By.XPATH, "//*[@id='contact-form-modal']/div[2]/form/div/div[5]/div").click()

                # By.XPATH, "//*[@data-testid='submit-button']").click()
                # By.XPATH, "/html/body/div[8]/div/div/div[2]/form/div/div[5]/div/button").click()
            
            # FULL XPATH - /html/body/div[7]/div/div/div[2]/form/div/div[5]/div/button
            # submitForm = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[@data-testid='submit-button']")))
            # submitForm.click()
            
            
            time.sleep(5)

            success_text = driver.find_element(
                By.XPATH, "//*[@id='contact-form-modal']/div[2]/div/div[1]/div/div/span/div").text

            if (success_text == "Your enquiry has been sent"):
                print("MESSAGE SENT TO AGENT!")
            else:
                print(success_text)
                error_notify(l)
                print("error Notifying Agent")

        except Exception as e:
            print(e)
            print(driver.page_source.encode("utf-8"))
            error_notify(l)
            print("error Notifying Agent")

    driver.close()

# Selenium UTILS


def login_daft(driver: Chrome):
    print("Navigating to login page")
    # driver.get("https://auth.daft.ie/auth/realms/daft/protocol/openid-connect/auth?client_id=daft-web-v1&scope=openid%20offline_access%20user_store&response_type=code&redirect_uri=https%3A%2F%2Fwww.daft.ie%2Fauth%2Fcallback&state=m4wtoEpLgZvXfook85fjhIRAC14oTbbqPO-6wdozGjE&callbackURL=https%3A%2F%2Fwww.daft.ie%2Fauth%2Fcallback&failureRedirect=%2F&code_challenge=4AvPPBB-omWQ-DAkixraB4IhvDh9cSfoR3kj5jI458s&code_challenge_method=S256")
    driver.get("https://daft.ie")

    time.sleep(1)

    # Accept Cookies Button
    driver.find_element(
        By.XPATH, "/html/body/div[1]/div/div/main/div/button[2]").click()

    time.sleep(1)
    # Navigate to Sign in PAGE <Clicking button>
    driver.find_element(
        By.XPATH, "/html/body/div[2]/div[2]/header/div/div[2]/div[3]/ul/li[2]/a").click()

    # printIN TO DAFT ACCOUNT
    driver.find_element(
        By.XPATH, "/html/body/div/div/div[5]/div/form/div[1]/input[1]").send_keys(os.getenv('daft_email'))
    driver.find_element(
        By.XPATH, "/html/body/div/div/div[5]/div/form/div[1]/input[2]").send_keys(os.getenv("daft_password"))

    print("Entering DAFT.IE Credentials")

    driver.find_element(
        By.XPATH, "/html/body/div/div/div[5]/div/form/div[2]/input").click()

    print("Pressing INPUT BUTTON")
