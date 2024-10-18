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

import webscraper
import sheets

def perform_update():
    '''
    The main loop of the script. This function is called every 10 minutes.
    '''
    # fetch the list of prospective members
    tq_members = webscraper.fetch_prospective_members()

    # check the google sheet and see if any of the prospective members are not already in it
    sheet_members = sheets.get_list_of_known_members()

    # make a list of members that are in the tq page but not in the sheet
    tq_emails = [member['email'] for member in tq_members]
    sheet_emails = [member['email'] for member in sheet_members]
    pending_members = list(set(tq_emails) - set(sheet_emails))

    # send those members the interest email, then add them to the sheet
    for member in pending_members:
        pass

perform_update()