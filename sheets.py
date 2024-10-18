'''
The functions in this file are used to interact with the Google Sheets API and
perform specific functions such as adding a new member, updating their status,
removing them, or fetching information about a specific member.

The sheet in question should be the current year's IEEE Membership sheet.
'''

import tomllib
import gspread

SCOPES = ['https://www.googleapis.com/auth/drive.file']

def get_spreadsheet_id() -> str:
    '''
    Gets the spreadsheet ID from the auth.toml file.
    '''
    with open('auth.toml', 'rb') as f:
        auth = tomllib.load(f)
        return auth['GoogleSheets']['spreadsheet_id']

def get_worksheet() -> gspread.Worksheet:
    '''
    Gets the worksheet that represents the current year's IEEE membership sheet.
    '''
    gc = gspread.oauth(credentials_filename='credentials.json')
    return gc.open_by_key(get_spreadsheet_id()).worksheet('Sheet1')

def get_list_of_known_members() -> list[dict[str, str]]:
    '''
    Gets a list of all the members in the current year's IEEE membership sheet.

    Returns a list of dictionaries, where each dictionary contains the attributes 'name', 'email', 'status', and 'status_date'.
    '''
    # connect to google sheets and get the worksheet
    worksheet = get_worksheet()
    names_list = worksheet.col_values(1)[1:]
    emails_list = worksheet.col_values(2)[1:]
    status_list = worksheet.col_values(4)[1:]
    status_dates_list = worksheet.col_values(5)[1:]
    
    # create a list of dictionaries, where each dictionary contains the attributes 'name', 'email', 'status', and 'status_date'
    member_info = []
    for names, emails, status, status_dates in zip(names_list, emails_list, status_list, status_dates_list):
        member_info.append({
            'name': names,
            'email': emails,
            'status': status,
            'status_date': status_dates
        })
    return member_info