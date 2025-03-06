'''
The functions in this file are used to interact with Gmail. It has functions for sending an
email to a new member, sending a reminder email, and checking the email account for new
membership status updates.
'''

from simplegmail import Gmail
from simplegmail.query import construct_query
import re
from log import logger
from settings import settings

def get_gmail() -> Gmail:
    '''
    Initializes gmail object.
    '''
    gmail = Gmail(client_secret_file='credentials.json')
    return gmail

def format_email(email_str: str, member: dict[str, str]) -> str:
    '''
    Takes the HTML for the email and replaces the placeholder text with the member's name and president's name.
    '''
    email_str = email_str.replace("%FIRST_NAME%", member['name'].split(' ')[0])
    
    # get president's name from settings and replace in email
    president_name = settings['Gmail']['president_name']
    email_str = email_str.replace("%PRESIDENT_NAME%", president_name)
    return email_str

def get_email(email_name: str) -> str:
    with open(f'emails/{email_name}.html', 'r') as f:
        email_str = f.read()
        return email_str

def send_interest_email(member: dict[str, str]):
    '''
    Sends an email to a new member.
    '''

    # load interest form
    email_html = get_email('interest')
    email_html = format_email(email_html, member)

    # send email to user
    gmail = get_gmail()
    params = {
        'to': member['email'],
        'sender': 'ieeesb@g.clemson.edu',
        'subject': 'Thank you for your interest in Clemson IEEE!',
        'msg_html': email_html,
        'signature': True,
    }

    if settings.get('Debug') != True:
        gmail.send_message(**params)

    logger.debug(f'Interest email sent to {member["name"]}')

def send_reminder_email(member: dict[str, str]):
    '''
    Sends a reminder email to a member.
    '''
    # load interest form
    email_html = get_email('reminder')
    email_html = format_email(email_html, member)

    # send email to user
    gmail = get_gmail()
    params = {
        'to': member['email'],
        'sender': 'ieeesb@g.clemson.edu',
        'subject': 'Clemson IEEE: Please Complete Registration Within One Week',
        'msg_html': email_html,
        'signature': True,
    }
    if settings.get('Debug') != True:
        gmail.send_message(**params)

    logger.debug(f'Reminder email sent to {member["name"]}')

def send_welcome_email(member: dict[str, str]):
    '''
    Sends a welcome email to a member.
    '''
    # load interest form
    email_html = get_email('welcome')
    email_html = format_email(email_html, member)

    # send email to user
    gmail = get_gmail()
    params = {
        'to': member['email'],
        'sender': 'ieeesb@g.clemson.edu',
        'subject': 'Welcome to IEEE!',
        'msg_html': email_html,
        'signature': True,
    }

    if settings.get('Debug') != True:
        gmail.send_message(**params)

    logger.debug(f'Welcome email sent to {member["name"]}')

def send_rejection_email(member: dict[str, str]):
    '''
    Sends a welcome email to a member.
    '''
    # load interest form
    email_html = get_email('rejection')
    email_html = format_email(email_html, member)

    # send email to user
    gmail = get_gmail()
    params = {
        'to': member['email'],
        'sender': 'ieeesb@g.clemson.edu',
        'subject': 'Clemson IEEE Student Branch: Your application has been rejected due to lack of information',
        'msg_html': email_html,
        'signature': True,
    }

    if settings.get('Debug') != True:
        gmail.send_message(**params)

    logger.debug(f'Rejection email sent to {member["name"]}')

def swap_email_ending(email):
    '''
    If email ends in @clemson.edu, returns the email ending with @g.clemson.edu.
    If email ends in @g.clemson.edu, returns the email ending with @clemson.edu.
    '''
    if email.endswith("@clemson.edu"):
        return email.replace("@clemson.edu", "@g.clemson.edu")
    elif email.endswith("@g.clemson.edu"):
        return email.replace("@g.clemson.edu", "@clemson.edu")
    else:
        return "Invalid email domain. Must be @clemson.edu or @g.clemson.edu."

def find_membership_number(email: str) -> str:
    '''
    Attempts to find a membership number in the email. Returns the membership number if found, otherwise returns None.
    '''
    # Regex pattern to match 9 or 10 digit numbers surrounded by spaces or punctuation
    pattern = r'(?<!\d)[\s.,!?;:"\'(){}\[\]\-\*\r\n]*(\d{9,10})(?=([\s.,!?;:"\'(){}\[\]\-\\r\\n\*]))'
    
    # Search for the first match
    match = re.search(pattern, email)
    
    # Return the matched number if found, otherwise return None
    if match:
        return match.group(1)
    return None

def get_membership_id_from_email(member: dict[str, str]) -> str:
    '''
    Takes a member and returns their membership ID from the email.
    '''
    query = construct_query({
        'sender': [member['email'], swap_email_ending(member['email'])],
    })

    gmail = get_gmail()
    messages = gmail.get_messages(query=query)

    # search all emails for the membership number
    # if the membership number is found, return it
    # if not, return None
    for message in messages:
        if find_membership_number(message.plain):
            return find_membership_number(message.plain)
    return None

def send_critical_email(message):
    '''
    Sends a critical email to ieeesb@g.clemson.edu informing the executive team that something has gone wrong.
    The message parameter will be included in the body of the email.
    '''

    email_html = get_email('critical')
    email_html = email_html.replace('%%MESSAGE%%', message)

    gmail = get_gmail()
    params = {
        'to': 'ieeesb@g.clemson.edu',
        'sender': 'ieeesb@g.clemson.edu',
        'subject': 'CRITICAL ERROR in IEEE Registration Bot',
        'msg_html': email_html,
        'signature': True
    }

    if settings.get('Debug') != True:
        gmail.send_message(**params)

    logger.debug(f'Sending critical error message to ieeesb@g.clemson.edu with message: {message}')

# print(get_membership_id_from_email({'name': 'Ignacio Carmichael', 'email': 'ignacic@clemson.edu'}))
# send_rejection_email({'name': 'David Bootle', 'email': 'dbootle@clemson.edu'})