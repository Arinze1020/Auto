import os
import sys
import random
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import (InvalidSessionIdException,
                                        NoSuchElementException,
                                        WebDriverException)
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from __constants__.const import password, email, api
from __functions__.functions import inject_input, scroll_click_element, switch_frame, click_element



agent='Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0'
API_KEY = api
data_sitekey = '6LdaB7UUAAAAAD2w3lLYRQJqsoup5BsYXI2ZIpFF'

def delay ():
    time.sleep(random.randint(2,3))


def Load_drive():
    options = webdriver.FirefoxOptions()
    options.headless = False
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--disable-web-security")
    #viewport = ['2560,1440', '1920,1080', '1440,900']
    options.add_argument("--ignore-certificate-error")
    options.add_argument("--ignore-ssl-errors")
    options.add_argument('--log-level=3')
    #options.add_argument('useAutomationExtension', False)
    options.add_argument('--disable-blink-features=AutomationControlled')
    #options.add_argument(f"user-agent={agent}")
    #options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])


    driver = webdriver.Firefox(options = options,executable_path=r'./webdriver/geckodriver')
    driver.implicitly_wait(30)
    return driver
    
def Job():
    url1 = 'https://all-access.wax.io/'
    url = 'https://r2.atomichub.io/drops/graffiti.r2'
    driver = Load_drive()
    main_page = driver.current_window_handle
    driver.get(url)
    scroll_click_element(driver, '/html/body/div[3]/div/div/div/div[2]/button[1]')
    click_element(driver, "/html/body/div/nav/div/div[4]/div/button")
    click_element(driver, "/html/body/div/div[1]/div/div[2]/div[1]/div[2]")
    time.sleep(15)


    for handle in driver.window_handles:
        if handle != main_page:
            login_page = handle
    
    driver.switch_to.window(login_page)
    scroll_click_element(driver, "(//input[@name='userName'])[2]")
    driver.find_element_by_xpath("(//input[@name='userName'])[2]").clear()

    driver.find_element_by_xpath("(//input[@name='userName'])[2]").send_keys(email)
    driver.find_element_by_xpath("(//input[@name='password'])[2]").clear()
    driver.find_element_by_xpath("(//input[@name='password'])[2]").send_keys(password)

    u1 = f"https://2captcha.com/in.php?key={API_KEY}&method=userrecaptcha&googlekey={data_sitekey}&pageurl={url1}&json=1&invisible=1"
    r1 = requests.get(u1)
    print(r1.json())
    rid = r1.json().get("request")
    u2 = f"https://2captcha.com/res.php?key={API_KEY}&action=get&id={int(rid)}&json=1"
    time.sleep(5)
    while True:
        r2 = requests.get(u2)
        print(r2.json())
        if r2.json().get("status") == 1:
            form_tokon = r2.json().get("request")
            break
        time.sleep(5)
    driver.execute_script(
        'document.getElementById("g-recaptcha-response-1").innerHTML = "%s"'% form_tokon
    )
    print('here')
    time.sleep(3)
    
    driver.execute_script("___grecaptcha_cfg.clients['1']['Z']['Z']['callback']('%s')"% form_tokon)
    print('submited')
    time.sleep(3)
   
    

    click_element(driver, "/html/body/div[1]/div/div/div[2]/div[5]/div/div/div/div[5]/button[1]")
    driver.switch_to.window(main_page)
    time.sleep(100)
    
    
    

if __name__ == "__main__":
    Job()
    Load_drive().close()
