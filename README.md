### The scraping part is broken (most prolly because of the changes in source code of slcm) this project is not currently active as I cant keep running on local due to some issues 

# slcm notifs
This is a simple script which scrapes the slcm uploaded and important document details and uploads them to instagram if any of them are not present in previously scraped data
## Setup Guide:
1. Install dependencies from requirements.txt , after installing all dependencies make sure to install headless browsers using `playwright install`
2. Setup .env similar to .env.example
3. run the main.py file and you are good to go
4. If you are working on other branches which have git-crypt encryption enabled make sure to read how to set it up [here](https://github.com/ninetynin/slcm_notifs/blob/5-sessionjson-encryption-issue-with-github-actions/docs/README-GIT-CRYPT.md) and make sure to not push your git-crypt encrypted key and for testing make sure to convert the secret into base64 and upload it as a secret

Currently only [branch](https://github.com/ninetynin/slcm_notifs/tree/local-cronjob) is running in local(every 1hr when the user is logged in) since there are issues with git-crypt encryption with workflow.
