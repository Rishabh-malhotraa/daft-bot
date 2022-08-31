import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from email_notification import error_notify


# Selenium Send Automted Response


def send_automated_response(listings):
    if len(listings) == 0:
        return

    # Uncomment for UBUNUTU
    # driver_location = "/usr/bin/chromedriver"
    # binary_location = "/usr/bin/google-chrome"

    # option = webdriver.ChromeOptions()
    # option.binary_location = binary_location

    # driver = webdriver.Chrome(
    #     executable_path=driver_location, chrome_options=option)

    driver = webdriver.Chrome()

    login_daft(driver)

    # SEND MESSAGE

    for l in listings:
        try:
            driver.get(l.daft_link)
            # Mail the AGENT Button
            driver.find_element(By.CLASS_NAME, "cWKcCS").click()
            time.sleep(1)
            driver.find_element(By.ID, "keyword1").send_keys(
                os.getenv('daft_name'))
            time.sleep(1)
            driver.find_element(By.ID, "keyword2").send_keys(
                os.getenv("daft_mail"))
            time.sleep(1)
            driver.find_element(By.ID, "keyword3").send_keys(
                os.getenv("daft_phone_number"))
            time.sleep(1)
            driver.find_element(By.ID, "message").send_keys(
                os.getenv("daft_text"))

        except:
            error_notify(l)
            print("error sending mail")

    driver.close()

# Selenium UTILS


def login_daft(driver):
    driver.get("https://daft.ie/")

    # Accept Cookies Button
    driver.find_element(
        By.XPATH, "/html/body/div[1]/div/div/main/div/button[2]").click()

    # Navigate to Sign in PAGE <Clicking button>
    driver.find_element(
        By.XPATH, "/html/body/div[2]/div[2]/header/div/div[2]/div[3]/ul/li[2]/a").click()

    # LOGIN TO DAFT ACCOUNT
    driver.find_element(
        By.XPATH, "/html/body/div/div/div[5]/div/form/div[1]/input[1]").send_keys("aarnav.iehs@gmail.com")
    driver.find_element(
        By.XPATH, "/html/body/div/div/div[5]/div/form/div[1]/input[2]").send_keys("PleaseGiveHouse@12468")

    driver.find_element(
        By.XPATH, "/html/body/div/div/div[5]/div/form/div[2]/input").click()
