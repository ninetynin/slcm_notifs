# slcm notifs

Setup Guide:
1. Install dependencies from requirements.txt , after installing all dependencies make sure to install headless browsers using `playwright install`
2. Setup .env similar to .env.example
3. run the main.py file and you are good to go
4. If you are working on other branches which have git-crypt encryption enabled make sure to read how to set it up [here](https://github.com/ninetynin/slcm_notifs/blob/5-sessionjson-encryption-issue-with-github-actions/docs/README-GIT-CRYPT.md)

Currently only [branch](https://github.com/ninetynin/slcm_notifs/tree/local-cronjob) is running in local since there are issues with git-crypt encryption with workflow.
