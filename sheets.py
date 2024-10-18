'''
The functions in this file are used to interact with the Google Sheets API and
perform specific functions such as adding a new member, updating their status,
removing them, or fetching information about a specific member.

The sheet in question should be the current year's IEEE Membership sheet.
'''

from datetime import datetime
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

def add_prospective_member_to_sheet(member: dict[str, str]):
    '''
    Takes a new prospective member and adds them to the current year's IEEE membership sheet.

    The member should be a dictionary with the attributes 'name', 'email'. The member
    will be given the status 'EMAIL SENT' with the current date.
    '''
    # connect to google sheets and get the worksheet
    worksheet = get_worksheet()

    # get the current date
    current_date = datetime.now().strftime('%m/%d/%Y')

    # add the new member to the sheet
    print(worksheet.append_row([member['name'], member['email'], '', 'EMAIL SENT', current_date], table_range='A1:E1'))

def update_member_status(member: dict[str, str], new_status: str):
    '''
    Takes a member and a new status, and updates the status of the member in the current year's IEEE membership sheet.

    The member should be a dictionary with the attributes 'name', 'email'. The new_status should be a string.
    '''
    # connect to google sheets and get the worksheet
    worksheet = get_worksheet()

    # get the current date
    current_date = datetime.now().strftime('%m/%d/%Y')

    # update the status of the member in the sheet
    cell = worksheet.find(member['email'])
    member_row = cell.row
    worksheet.update_cell(member_row, 4, new_status)
    worksheet.update_cell(member_row, 5, current_date)

def member_approved(member: dict[str, str], member_id: str):
    '''
    Updates the status of the member to 'APPROVED' and adds their membership ID to the members sheet.

    Member should be a dictionary with the attributes 'name', 'email'. member_id should be a string.
    '''
    # connect to google sheets and get the worksheet
    worksheet = get_worksheet()

    # get the current date
    current_date = datetime.now().strftime('%m/%d/%Y')

    # update the status of the member in the sheet
    cell = worksheet.find(member['email'])
    member_row = cell.row
    worksheet.update_cell(member_row, 3, member_id)
    worksheet.update_cell(member_row, 4, 'APPROVED')
    worksheet.update_cell(member_row, 5, current_date)

def remove_member(member: dict[str, str]):
    '''
    Remove member from members sheet.

    Member should be a dictionary with the attributes 'name', 'email'.
    '''
    # connect to google sheets and get the worksheet
    worksheet = get_worksheet()

    # get the current date
    current_date = datetime.now().strftime('%m/%d/%Y')

    # update the status of the member in the sheet
    cell = worksheet.find(member['email'])
    member_row = cell.row
    worksheet.delete_rows(member_row, member_row)

# add_prospective_member_to_sheet({'name': 'David Bootle', 'email': 'dbootle@clemson.edu'})
# update_member_status({'name': 'David Bootle', 'email': 'dbootle@clemson.edu'}, 'REMINDER SENT')
# member_approved({'name': 'David Bootle', 'email': 'dbootle@clemson.edu'}, '123456789')
# remove_member({'name': 'David Bootle', 'email': 'dbootle@clemson.edu'})