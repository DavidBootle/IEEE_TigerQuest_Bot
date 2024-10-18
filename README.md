# IEEE_TigerQuest_Bot
Automatically checks for new members on the IEEE TigerQuest and adds them 

## Installation and Setup
1. Run `python -m venv .venv` to create a virtual environment in the current directory then enter it using `source .venv/bin/activate`.

2. Run the following commands to install required libraries:
```bash
pip install selenium
```

3. Create an `auth.toml` file in the project folder with the following info:
```toml
[ClemsonAuth]
username = "your username"
password = "your password"
```