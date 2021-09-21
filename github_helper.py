#create personal access token: https://docs.github.com/en/github/authenticating-to-github/keeping-your-account-and-data-secure/creating-a-personal-access-token
from github import Github
import os
import requests
import re

"""
GithubHelper is a wrapper class for any ease of use functions related to accessing the GitHub API.
"""
class GithubHelper:
    def __init__(self, token):
        self.gh = Github(token)

    """
    Get a list of all repos from the specified organization.
    Only returns repo names that match the optional regex if supplied, otherwise fetches all.
    """
    def get_all_organization_repos(self, organization, regex=None):
        repos = self.gh.get_organization(organization).get_repos(type='all')
        if regex:
            regex_filter = re.compile(regex)
            matched = []
            for repo in repos:
                if regex_filter.search(repo.full_name):
                    matched.append(repo)
            repos = matched
        return repos
