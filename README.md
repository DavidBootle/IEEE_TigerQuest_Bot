# IEEE_TigerQuest_Bot
Automatically checks for new members on the IEEE TigerQuest and adds them 

## Installation and Setup
1. Run `python -m venv .venv` to create a virtual environment in the current directory then enter it using `source .venv/bin/activate`.

2. Run the following commands to install required libraries:
```bash
pip install selenium gspread simplegmail
```

3. Create an `auth.toml` file in the project folder with the following info:
```toml
[ClemsonAuth]
username = "your username"
password = "your password"

[GoogleSheets]
spreadsheet_id = 'spreadsheet id'

[Gmail]
president_name = 'president name'
```

4. Download your credentials as a .json file from the Google API Console and save them to a file called `credentials.json` in the project folder.

5. When you run the script for the first time, it will ask you to authorize it using your Google account. Always authorize it with the ieeesb@g.clemson.edu account. DO NOT use your personal account, as that will break it. If authentication is failing, delete the `token.json` file in the current directory and try again.