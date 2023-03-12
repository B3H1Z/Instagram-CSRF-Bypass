import time

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import os

clear = lambda: os.system('cls')

# Download Webdriver automatically And Make an object
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

driver.get("https://instagram.com")


def login(username, password):
    csrf_status = set_csrf_cookie()
    if not csrf_status:
        driver.quit()

    input_username = driver.find_element(By.NAME, "username")
    input_password = driver.find_element(By.NAME, "password")

    input_username.send_keys(Keys.CONTROL, "a", Keys.DELETE)
    input_password.send_keys(Keys.CONTROL, "a", Keys.DELETE)

    input_username.send_keys(username)
    input_password.send_keys(password)

    input_password.submit()
    time.sleep(5)

    try:
        status_login = driver.find_element(By.ID, "slfErrorAlert")
    except:
        status_login = False

    if not status_login:
        clear()
        print("Successful Login")
        return True
    else:
        clear()
        print("Username or password was incorrect")
        return False


def set_csrf_cookie():
    if not driver.get_cookie('csrftoken'):

        csrf_token_exp_date = driver.execute_script(
            "return n=new Date; t=n.getTime(); et=t+36E9;n.setTime(et); n.toUTCString();")
        csrf_token = driver.execute_script(
            """ return document.body.innerHTML.split('csrf_token')[1].split('\\"')[2].slice(0,-1) """)

        driver.add_cookie(
            {"name": "csrftoken", "value": csrf_token, "expires": csrf_token_exp_date, 'path': '/',
             "domain": ".instagram.com"})

        csrf_cookie = driver.get_cookie('csrftoken')

        if csrf_cookie:
            print(f"Your csrf cookie:  {csrf_cookie}")
            return True
        else:
            print("Cannot create csrf token")
            return False


def run():
    login_status = False
    while not login_status:
        USERNAME = input("ENTER USERNAME: ")
        PASSWORD = input("ENTER PASSWORD: ")
        login_status = login(USERNAME, PASSWORD)


run()
time.sleep(20)
