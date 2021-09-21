# grader_helper

You must create a personal access token to use the GitHub API.  See the following for how to create a personal access token on GitHub:
https://docs.github.com/en/github/authenticating-to-github/keeping-your-account-and-data-secure/creating-a-personal-access-token

You need to create a local config file to store your personal access token for GitHub access.  The file should be created in the root directory and called "local_config.py".  It should contain a single global variable as follows:
MY_GITHUB_TOKEN = "your token string from github"

This file is already in the gitignore to prevent anyone sharing their PAT by mistake.

grader_helper.py is the main file, so execute with:
python grader_helper.py