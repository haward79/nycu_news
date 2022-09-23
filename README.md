# What's this
This is a news push program.  
This program collect news from https://infonews.nycu.edu.tw/ and the news will send to specific email address.

# Pre-requirements

- Software
  - Linux based OS
    - *Note: This program may run on Windows by modifying some codes.*
  - Python 3
  - Python 3 Library - feedparser, smtplib, email
    - *Note: You can install them by pip.*
  - Mail Trasfer Agent
  - cron

# Install

## Install cron
Please install main.py to cron.

Example config:
```
# m  h  dom mon dow   command
  0  *   *   *   *    python3 /home/user/Routine/nycu_news/main.py
```

## Change mail info
Use text editor to open main.py and edit the following code:
```
mail_sender = 'sender@example.com'
mail_receiver = 'user@example.com'
```
Please change 'user@example.com' and 'sender@example.com' to the correct mail sender and receiver.


# Changelog
- 09 / 24 2022
  - Modify error handling method. Error messages is included to the mail content.

- 05 / 26 2022
  - Fix a bug: Decode type changed from big5 to cp950.

- 04 / 21 2022
  - Fix a bug: Decode type changed from big5 to cp950.

- 02 / 20 2022
  - Fix a bug: Send mail even if there is no news.
  
- 02 / 19 2022
  - Fix a bug: Catch exception for failure of the website.
  
- 02 / 18 2022
  - First commit.
  - Program is ready to use.

# Copyright
This program is written by [haward79](https://www.haward79.tw/).  
All rights reserved by haward79.

