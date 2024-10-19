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
import gmail
from datetime import datetime

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

    '''NEW MEMBERS'''
    # send those members the interest email, then add them to the sheet
    for member in pending_members:
        gmail.send_interest_email(member)
        sheets.add_prospective_member_to_sheet(member)
    
    '''CHECK FOR MEMBER RESPONSES IN THE EMAIL'''
    # for each member in tigerquest, check to see if they have emailed their membership status
    for member in sheet_members:
        # if the member is on the tq page, see if they have emailed their membership status
        if member['email'] in tq_emails:
            id = gmail.get_membership_id_from_email(member)
            if id is not None:
                # if they have emailed their membership status, update their status in the sheet and accept them in tigerquest and email them the welcome message
                webscraper.accept_member(member)
                sheets.member_approved(member, id)
                gmail.send_welcome_email(member)
    
    # refresh member list
    tq_members = webscraper.fetch_prospective_members() # fetch the list of prospective members
    sheet_members = sheets.get_list_of_known_members() # check the google sheet and see if any of the prospective members are not already in it
    
    '''SEND REMINDERS'''
    # get a list of members that are in the sheet, but have a status of 'EMAIL SENT' and a status date more than a week ago
    for member in sheet_members:
        # if the member was sent an email more than a week ago, send a reminder email and change their status to 'REMINDER SENT'
        if member['status'] == 'EMAIL SENT' and (datetime.now() - datetime.strptime(member['status_date'], '%m/%d/%Y')).days > 7:
            gmail.send_reminder_email(member)
            sheets.update_member_status(member, 'REMINDER SENT')

    '''REMOVE MEMBERS WHO HAVE CANCELLED THEIR MEMBERSHIP'''
    # Find members who are not on the tq page, but do not have a status of 'APPROVED'. If they cancelled their own membership, they should be removed from the sheet.
    cancelled_members = [member for member in sheet_members if member['email'] not in tq_emails and member['status'] != 'APPROVED']
    for member in cancelled_members:
        sheets.remove_member(member)
    
    '''REJECT MEMBERS WHO HAVE NOT RESPONDED WITHIN THE TIME LIMIT'''
    # get a list of members that are in the sheet and on the tq page, but have a status of 'REMINDER SENT' and a status date more than a week ago
    members_to_remove_from_tq = []
    for member in sheet_members:
        # if the member was sent a reminder more than a week ago
        if member['status'] == 'REMINDER SENT' and (datetime.now() - datetime.strptime(member['status_date'], '%m/%d/%Y')).days > 7:
            # if the member is on the tq page, reject them and remove them from the sheet
            if member['email'] in tq_emails:
                members_to_remove_from_tq.append(member)
            # remove them from the sheet
            sheets.remove_member(member)
    webscraper.reject_members(members_to_remove_from_tq)

perform_update()