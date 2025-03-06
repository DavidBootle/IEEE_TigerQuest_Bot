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
from selenium.common.exceptions import NoSuchElementException
from settings import settings
from time import sleep
from log import logger

PROSPECTIVE_MEMBER_URL = settings['TigerQuest']['prospective_member_url']
LOGIN_DOMAIN = settings['ClemsonAuth']['login_domain']

'''UTILITY FUNCTIONS'''
def initialize_driver() -> webdriver.Chrome:
    '''
    Returns a webdriver object for the TigerQuest prospective member page.
    AKA Opens a new chrome browser.
    '''
    path = settings['SeleniumDriver']['path']
    if path == '':
        path = None
    service = webdriver.ChromeService(executable_path=path)
    driver = webdriver.Chrome(service=service)
    return driver

def selenium_test():
    '''
    Tests the selenium driver by opening the TigerQuest prospective member page.
    '''
    driver = initialize_driver()
    driver.get(PROSPECTIVE_MEMBER_URL)
    input("Press Enter to continue...")
    driver.close()

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
        username = settings['ClemsonAuth']['username']
        password = settings['ClemsonAuth']['password']
        # type the username and password into the login form
        driver.find_element(By.ID, 'username').send_keys(username)
        driver.find_element(By.ID, 'password').send_keys(password)
        sleep(2) # sleep for 2 seconds
        driver.find_element(By.ID, 'submitButton').click()

def wait_for_member_list(driver: webdriver.Chrome):
    '''
    Waits for the element with svg class (tigerquest roster page list)
    '''
    try:
        logger.debug('Waiting for svgGrid (member listings) to appear...')
        WebDriverWait(driver, 60).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'svgGrid')))
        logger.debug('Found svgGrid, continuing after one second...')
        sleep(1) # wait one second just to be sure
    except TimeoutError:
        logger.error("Failed to find svgGrid (member listings) within 60 seconds.")
        raise TimeoutError("Failed to find list of members within 60 seconds.")

def load_prospective_member_page(driver: webdriver.Chrome):
    '''
    Opens the prospective member page in TigerQuest and logs in if necessary.
    '''
    logger.debug('Loading propsective members page.')
    driver.get(PROSPECTIVE_MEMBER_URL)

    # login if necessary
    clemson_login(driver)

    # wait for the member grid to load
    wait_for_member_list(driver)

def fetch_prospective_members() -> list[dict[str, str]]:
    '''
    Opens the TigerQuest page and returns a list of the prospective members.
    The returned object is a list of dictionaries, where each dictionary contains
    the attributes 'name' and 'email'.
    '''
    logger.info('Fetching prospective members...')
    driver = initialize_driver() # Create a new webdriver
    load_prospective_member_page(driver) # open TigerQuest page

    # get a list of all the member-modal class elements that are links, as they contain the names of the users

    member_info = []

    def get_member_info_for_page():
        # double check the member grid exists
        wait_for_member_list(driver)

        # find all elements identified by a.member-modal
        name_elements = driver.find_elements(By.XPATH, "//table//a[contains(@class, 'member-modal')]")

        # extract the href attributes from each element
        name_element_hrefs = [element.get_attribute('href') for element in name_elements]

        # for each url, open in a new tab and extract the name and email, then save to member info
        for url in name_element_hrefs:
            logger.debug(f'Opening window to get information for url {url}')
            # open a new tab with javascript
            driver.execute_script("window.open('');")

            # switch to the new tab
            driver.switch_to.window(driver.window_handles[-1])

            # navigate to the new URL in the new tab
            driver.get(url)

            # wait for the page to load
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'userCard-section')))

            # get the name and email from the new tab
            name = driver.find_element(By.CSS_SELECTOR, 'span.fn').text
            email = driver.find_element(By.CSS_SELECTOR, 'a.email').get_attribute('href')[7:]
            member_info.append({
                'name': name,
                'email': email
            })

            logger.debug(f'Found info for member {name}')

            # close the current tab
            driver.close()

            # switch back to original tab
            driver.switch_to.window(driver.window_handles[0])
        
        # check to see if the next button is present, and if so, click it and call the function again
        try:
            next_button = driver.find_element(By.XPATH, "//span[@class='paginationRight']//a[text()='next']")
            # if this didn't fail, then the next button is present, click it and call the function again
            logger.debug('Found next page button, moving to next page...')
            driver.get(next_button.get_attribute('href'))
            get_member_info_for_page()
        except NoSuchElementException:
            # if the next button is not present, then we're done
            logger.debug("Didn't find next page button. We're done here!")
            return
    
    get_member_info_for_page()
    driver.close()
    return member_info

def get_member_page_id(driver: webdriver.Chrome, name: str):
    '''
    Returns the id of the member's page on the TigerQuest page.
    '''
    # find the checkbox with the correct id and extract it
    try:
        id = driver.find_element(By.CSS_SELECTOR, f"input[title='{name}']").get_attribute('value')
        return id
    except NoSuchElementException:
        return None

def accept_member(driver: webdriver.Chrome, member: dict[str, str]):
    '''
    Accepts a member by clicking the reject button on the TigerQuest page.
    Does not load the tigerQuest page.
    '''
    logger.debug(f'Accepting member {member["name"]}...')
    load_prospective_member_page(driver)
    wait_for_member_list(driver)

    def attempt_to_accept():
        # find the id for the specific member
        id = get_member_page_id(driver, member['name'])
        if id is None:
            # the id is not found on this page, go to the next page
            try:
                next_button = driver.find_element(By.XPATH, "//span[@class='paginationRight']//a[text()='next']")
                # if this didn't fail, then the next button is present, click it and call the function again
                driver.get(next_button.get_attribute('href'))
                attempt_to_accept()
                return
            except NoSuchElementException:
                # if the next button is not present, then we're done
                logger.debug(f'Failed to find member {member["name"]} on TigerQuest to accept.')
                return
            
        # if the id is found
        else:
            # run javascript to accept the user
            if settings.get('Debug') != True:
                driver.execute_script(f"ApproveMember('https://clemson.campuslabs.com/engage/actioncenter/organization/ieee_sbinactive/roster/roster/approvemember/{id}');")
    
    attempt_to_accept()

def accept_members(members: list[dict[str, str]]):
    '''
    accepts a list of members by clicking the accept button on the TigerQuest page.
    '''
    driver = initialize_driver()

    for member in members:
        accept_member(driver, member)
    
    driver.close()

def reject_member(driver: webdriver.Chrome, member: dict[str, str]):
    '''
    Rejects a member by clicking the reject button on the TigerQuest page.
    Does not load the tigerQuest page.
    '''
    logger.debug(f'Rejecting member {member["name"]}...')
    load_prospective_member_page(driver)
    wait_for_member_list(driver)

    def attempt_to_remove():
        # find the id for the specific member
        id = get_member_page_id(driver, member['name'])
        if id is None:
            # the id is not found on this page, go to the next page
            try:
                next_button = driver.find_element(By.XPATH, "//span[@class='paginationRight']//a[text()='next']")
                # if this didn't fail, then the next button is present, click it and call the function again
                driver.get(next_button.get_attribute('href'))
                attempt_to_remove()
                return
            except NoSuchElementException:
                # if the next button is not present, then we're done
                logger.debug(f'Failed to find member {member["name"]} on TigerQuest to remove.')
                return
            
        # if the id is found
        else:
            # run javascript to reject the user
            if settings.get('Debug') != True:
                driver.execute_script(f"DenyMember('https://clemson.campuslabs.com/engage/actioncenter/organization/ieee_sbinactive/roster/roster/denymember/{id}');")
    
    attempt_to_remove()

def reject_members(members: list[dict[str, str]]):
    '''
    Rejects a list of members by clicking the reject button on the TigerQuest page.
    '''
    driver = initialize_driver()

    for member in members:
        reject_member(driver, member)
    
    driver.close()
