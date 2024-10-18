'''
IEEE TigerQuest Bot
David Bootle 2024

This script will automatically check the TigerQuest registration page for new member applications.
If they are new, it will send them a interest email. If they are not new, it will check their status
and send them a reminder email one week after the interest email was sent. If it has been more than a
week since the reminder email was sent, their application will be rejected and they will be removed
from the google sheet. The script will also periodically check the ieeesb@g.clemson.edu email account
for members responding with their IEEE membership status, and will automatically add them to the google sheet and accept them into TigerQuest.

This project uses the Google Sheets API, the Gmail API, and selenium in order to access TigerQuest.
Authorization scope for the project's APIs can be found on google cloud under the
ieeesb@g.clemson.edu email address.
'''

from webscraper import *

driver = initialize_driver()
load_prospective_member_page(driver)
input()
