# IEEE_TigerQuest_Bot
Automatically checks for new members on the IEEE TigerQuest and adds them 

## Installation and Setup
1. Run `python -m venv .venv` to create a virtual environment in the current directory then enter it using `source .venv/bin/activate`.

2. Run the following commands to install required libraries:
```bash
pip install selenium gspread simplegmail tdqm
```

3. Create an `auth.toml` file in the project folder with the following info:
```toml
Debug = false # if true, will not make permanent changes

[System]
sleep_minutes = 5 # Number of minutes to sleep between checks (recommended 5-10)

[ClemsonAuth]
login_domain = 'idpfed.clemson.edu'
username = "your username"
password = "your password"

[GoogleSheets]
spreadsheet_id = 'spreadsheet id' # id of the spreadsheet to keep track of members on

[Gmail]
president_name = 'president name'

[SeleniumDriver]
path = '' # path to the chromedriver executable or empty string for auto selection
# if you get weird issues related to the chromedriver, manually set this value

[TigerQuest]
prospective_member_url = 'https://clemson.campuslabs.com/engage/actioncenter/organization/ieee_sb/roster/Roster/prospective'
approve_member_url = 'https://clemson.campuslabs.com/engage/actioncenter/organization/ieee_sb/roster/roster/approvemember/'
reject_member_url = 'https://clemson.campuslabs.com/engage/actioncenter/organization/ieee_sb/roster/roster/denymember/'
```

4. Download your credentials as a .json file from the Google API Console and save them to a file called `credentials.json` in the project folder. You must sign into the Google API Console as ieeesb@g.clemson.edu. You should see a project called IEEE Registration Bot. Go to the [credentials page](https://console.cloud.google.com/apis/credentials) and click the download button for the OAuth 2.0 Client IDs.

5. When you run the script for the first time, it will ask you to authorize it using your Google account. Always authorize it with the ieeesb@g.clemson.edu account. DO NOT use your personal account, as that will break it. If authentication is failing, delete the `token.json` file in the current directory and try again.

## Debug Mode
When testing the program, you can edit the following line at the **top** of the `auth.toml` file to enable debug mode:

```toml
Debug = true
```

This will **prevent the program from taking any permanent actions**, such as updating the google sheet, sending emails, or accepting or rejecting members. In addition, the output log will contain more detailed information, similar to the `registration.log` file. Note that the console output will still log things like "email sent" and "accepted member", but the actual action will not be performed.

Debug mode is intended to be used when testing and debugging logic in the program. Please make sure to test without debug mode when trying to catch any bugs related to the webdriver, google sheets, or gmail APIs, as these services may not be used fully in debug mode.