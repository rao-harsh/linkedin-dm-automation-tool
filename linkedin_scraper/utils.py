from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time
import logging
import datetime
import random


linkedin_url = 'https://www.linkedin.com/login'

# //span[@class="artdeco-button__text" and text()="Connect"]


class AlreadyConnectedProfileException(Exception):
    def __init__(self, msg) -> None:
        self.msg = msg


class ProfileNotFoundException(Exception):
    def __init__(self, msg):
        self.msg = msg


def find_connect_button(driver, delay):
    connect = safe_extract(
        driver, "//button[@class='artdeco-button artdeco-button--2 artdeco-button--primary ember-view pvs-profile-actions__action']")

    if connect is not None and connect.text.lower() == "connect":
        return connect

    time.sleep(delay)

    more_option = driver.find_elements(
        By.XPATH, "//div[@class=\"artdeco-dropdown artdeco-dropdown--placement-bottom artdeco-dropdown--justification-left ember-view\"]")[1]

    more_option.click()

    time.sleep(delay)

    connect = driver.find_elements(
        By.XPATH, "//span[@class=\"display-flex t-normal flex-1\" and text()=\"Connect\"]")

    connect = connect[1] if isinstance(
        connect, list) and len(connect) > 1 else None

    if connect is not None and connect.text.lower() == "connect":
        return connect

    connect = safe_extract(
        driver, '//button[@class="artdeco-button artdeco-button--2 artdeco-button--secondary ember-view pvs-profile-actions__action"]')

    if connect is not None and connect.text.lower() == "connect":
        return connect

    return None


# Configure logging for successful connections
successful_logging = logging.getLogger("successful")
successful_logging.setLevel(logging.INFO)
successful_handler = logging.FileHandler(
    "./logs/successful_linkedin_connections.log")
successful_handler.setFormatter(logging.Formatter("%(asctime)s - %(message)s"))
successful_logging.addHandler(successful_handler)


# Configure logging for unsuccessful connections
unsuccessful_logging = logging.getLogger('unsuccessful')
unsuccessful_logging.setLevel(logging.INFO)
unsuccessful_handler = logging.FileHandler(
    './logs/unsuccessful_linkedin_connections.log')
unsuccessful_handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(levelname)s - %(message)s'))
unsuccessful_logging.addHandler(unsuccessful_handler)


def set_delay(delay, auto_delay):
    return delay if auto_delay is False else random.randint(1, 30)


def connect_and_send_message(email, password, file_path, auto_delay=True, delay=1):
    delay = set_delay(delay, auto_delay)
    success_urls = []
    success_messages = []
    options = Options()
    options.add_argument("--headless=new")
    unsuccess_urls = []
    error_messages = []
    try:
        df = pd.read_excel(file_path)
        links, messages = df["Linkedin_Handle"], df["message"]
        details = [{"link": link, "message": message}
                   for link, message in zip(links, messages)]

        # Open the LinkedIn login page
        # Create a webdriver instance (e.g., Chrome)
        driver = webdriver.Chrome(options=options)
        driver.get(linkedin_url)
        logging.info("Opened LinkedIn login page")

        email_field = driver.find_element(By.ID, 'username')
        password_field = driver.find_element(By.ID, 'password')

        email_field.send_keys(email)
        time.sleep(delay)
        delay = set_delay(delay, auto_delay)
        password_field.send_keys(password)
        time.sleep(delay)
        delay = set_delay(delay, auto_delay)
        password_field.send_keys(Keys.ENTER)

        successful_count = 0
        unsuccessful_count = 0

        for detail in details:
            delay = delay if auto_delay is False else random.randint(1, 30)
            try:
                driver.find_element(By.TAG_NAME, 'body').send_keys(
                    Keys.CONTROL + 't')
                driver.get(detail["link"])
                # driver.get("https://www.linkedin.com/in/martasmiech/")
                time.sleep(delay)
                delay = set_delay(delay, auto_delay)
                not_found = safe_extract(
                    driver, '//h2[@class="ember-view artdeco-empty-state__headline artdeco-empty-state__headline--mercado-error-server-large artdeco-empty-state__headline--mercado-spots-large"]')
                if not_found:
                    logging.error(f"Profile Not found {detail['link']}")
                    unsuccessful_logging.error(
                        f"Profile Not found {detail['link']}")
                    raise ProfileNotFoundException(msg="Profile Not Found")
                logging.info(f"Visited Profile: {detail['link']}")
                time.sleep(delay)
                delay = set_delay(delay, auto_delay)

                connect = find_connect_button(driver, delay=delay)
                if connect is None:
                    raise AlreadyConnectedProfileException(
                        msg="Profile is already connected with provided account")

                connect.click()
                logging.info("Profile Connected Successfully")

                add_note = safe_extract(
                    driver, "//button[@aria-label='Add a note']")

                if add_note is None:
                    raise NoSuchElementException(
                        msg="Add Note button is not found there's some changes in LinkedIn UI")

                add_note.click()

                logging.info("Clicked Add Note Button")
                textbox = safe_extract(
                    driver, "//textarea[@name='message']")

                if textbox is None:
                    raise NoSuchElementException(
                        msg="textbox not found there's some changes in LinkedIn UI")

                textbox.send_keys(detail["message"])
                sendbutton = safe_extract(
                    driver, "//button[@aria-label='Send now']")

                if sendbutton is None:
                    raise NoSuchElementException(
                        msg="Send button is not found there's some changes in LinkedIn UI")

                sendbutton.click()
                successful_logging.info(
                    f"Connection Request sent successfully to {detail['link']}")
                success_urls.append(detail["link"])
                success_messages.append(
                    f"Connection Request sent successfully to {detail['link']}")
                successful_count += 1
            except ProfileNotFoundException as e:
                logging.error(f"Profile not Found {detail['link']}")
                unsuccess_urls.append(detail["link"])
                error_messages.append(
                    f"Profile not Found {detail['link']}")
                unsuccessful_logging.error(
                    f"Profile not Found {detail['link']}")
                unsuccessful_count += 1
            except AlreadyConnectedProfileException as e:
                logging.error(f"Profile is already connected {detail['link']}")
                unsuccess_urls.append(detail["link"])
                error_messages.append(
                    f"Profile is already connected {detail['link']}")
                unsuccessful_logging.error(
                    f"Profile is already connected {detail['link']}")
                unsuccessful_count += 1
            except NoSuchElementException as e:
                logging.error(f"Element not found: {e.msg}")
                unsuccessful_count += 1
                unsuccess_urls.append(detail["link"])
                error_messages.append(
                    f"Profile: {detail['link']} - Error: {e.msg}")
                unsuccessful_logging.error(
                    f"Profile: {detail['link']} - Error: {e.msg}")
            except Exception as e:
                unsuccessful_count += 1
                unsuccess_urls.append(detail["link"])
                error_messages.append(
                    f"Profile: {detail['link']} - Error: {e.args}")
                unsuccessful_logging.error(
                    f"Profile: {detail['link']} - Error: {e.args}")

        success_data = {"Linkedin_Handle": success_urls,
                        "success_message": success_messages}

        error_data = {"Linkedin_Handle": unsuccess_urls,
                      "error_message": error_messages}
        success_df = pd.DataFrame(success_data)
        error_df = pd.DataFrame(error_data)
        pd.set_option("display.max_colwidth", None)

        now = datetime.datetime.now()
        formatted_date = now.strftime("%Y-%m-%d %H:%M:%S,%f")
        success_excel_file_path = f"./reports/successful/success-{formatted_date}.xlsx".replace(
            ":", "_").replace(",", "_")
        error_excel_file_path = f"./reports/unsuccessful/unsuccess-{formatted_date}.xlsx".replace(
            ":", "_").replace(",", "_")

        success_df.to_excel(success_excel_file_path, index=False)
        error_df.to_excel(error_excel_file_path, index=False)

        logging.info(f"Total Successful Count: {successful_count}")
        logging.info(f"Total Unsuccessful Count: {unsuccessful_count}")
        return successful_count, unsuccessful_count, [success_excel_file_path, error_excel_file_path]
    except Exception as e:
        logging.error(
            f"An error occurred during the main execution: {e.args}")


def safe_extract(element, xpath):
    try:
        extracted_element = element.find_element(By.XPATH, xpath)
        return extracted_element
    except NoSuchElementException:
        return None


if __name__ == "__main__":
    connect_and_send_message("hannahjenkins512@gmail.com",
                             "hrao0905@HR", "./lu.xlsx")
