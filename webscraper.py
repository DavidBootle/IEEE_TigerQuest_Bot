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
from selenium.common.exceptions import NoSuchElementException

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

def fetch_prospective_members() -> list[dict[str, str]]:
    '''
    Opens the TigerQuest page and returns a list of the prospective members.
    The returned object is a list of dictionaries, where each dictionary contains
    the attributes 'name' and 'email'.
    '''
    
    driver = initialize_driver() # Create a new webdriver
    load_prospective_member_page(driver) # open TigerQuest page

    # get a list of all the member-modal class elements that are links, as they contain the names of the users

    member_info = []

    def get_member_info_for_page():
        # find all elements identified by a.member-modal
        name_elements = driver.find_elements(By.XPATH, "//table//a[contains(@class, 'member-modal')]")

        # extract the href attributes from each element
        name_element_hrefs = [element.get_attribute('href') for element in name_elements]

        # for each url, open in a new tab and extract the name and email, then save to member info
        for url in name_element_hrefs:
            # open a new tab with javascript
            driver.execute_script("window.open('');")

            # switch to the new tab
            driver.switch_to.window(driver.window_handles[-1])

            # navigate to the new URL in the new tab
            driver.get(url)

            # get the name and email from the new tab
            name = driver.find_element(By.CSS_SELECTOR, 'span.fn').text
            email = driver.find_element(By.CSS_SELECTOR, 'a.email').get_attribute('href')[7:]
            member_info.append({
                'name': name,
                'email': email
            })

            # close the current tab
            driver.close()

            # switch back to original tab
            driver.switch_to.window(driver.window_handles[0])
        
        # check to see if the next button is present, and if so, click it and call the function again
        try:
            next_button = driver.find_element(By.XPATH, "//span[@class='paginationRight']//a[text()='next']")
            # if this didn't fail, then the next button is present, click it and call the function again
            driver.get(next_button.get_attribute('href'))
            get_member_info_for_page()
        except NoSuchElementException:
            # if the next button is not present, then we're done
            return
    
    get_member_info_for_page()
    driver.close()
    return member_info