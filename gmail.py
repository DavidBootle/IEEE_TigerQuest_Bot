'''
The functions in this file are used to interact with Gmail. It has functions for sending an
email to a new member, sending a reminder email, and checking the email account for new
membership status updates.
'''

from simplegmail import Gmail
import tomllib

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
    
    # get president's name from auth.toml
    with open('auth.toml', 'rb') as f:
        auth = tomllib.load(f)
        president_name = auth['Gmail']['president_name']
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

    gmail.send_message(**params)

send_interest_email({'name': 'David Bootle', 'email': 'dbootle@clemson.edu'})
