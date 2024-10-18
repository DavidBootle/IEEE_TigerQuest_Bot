'''
The functions in this file are used to interact with selenium so that the bot can
check the TigerQuest registration page. Unfortunately, there does not appear to be developer
API for TigerQuest, and the site appears to be rendered on the server side. This is great
for security, and not great for somebody trying to make a hacky automation script.
'''

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import tomllib

PROSPECTIVE_MEMBER_URL = 'https://clemson.campuslabs.com/engage/actioncenter/organization/ieee_sbinactive/roster/Roster/prospective'
LOGIN_DOMAIN = 'idpfed.clemson.edu'

def selenium_test():
    '''
    Tests the selenium driver by opening the TigerQuest prospective member page.
    '''
    driver = webdriver.Chrome()
    driver.get(PROSPECTIVE_MEMBER_URL)
    input("Press Enter to continue...")
    driver.close()

'''UTILITY FUNCTIONS'''
def initialize_driver() -> webdriver.Chrome:
    '''
    Returns a webdriver object for the TigerQuest prospective member page.
    AKA Opens a new chrome browser.
    '''
    driver = webdriver.Chrome()
    return driver

def page_has_loaded(driver):
    '''
    Will return True if the page has loaded, False otherwise.
    '''
    return driver.execute_script("return document.readyState") == 'complete'

def clemson_login(driver: webdriver.Chrome):
    '''
    If on the Clemson login screen, logs in. Otherwise it does nothing.
    '''
    # check if the page is redirected to the login page
    if LOGIN_DOMAIN in driver.current_url:
        # if it is, log in using the credentials in the auth.toml file
        with open('auth.toml', 'rb') as f:
            auth = tomllib.load(f)
            username = auth['ClemsonAuth']['username']
            password = auth['ClemsonAuth']['password']
        # type the username and password into the login form
        driver.find_element(By.ID, 'username').send_keys(username)
        driver.find_element(By.ID, 'password').send_keys(password)
        driver.find_element(By.ID, 'submitButton').click()

def load_prospective_member_page(driver: webdriver.Chrome):
    '''
    Opens the prospective member page in TigerQuest and logs in if necessary.
    '''
    driver.get(PROSPECTIVE_MEMBER_URL)

    # login if necessary
    clemson_login(driver)

    