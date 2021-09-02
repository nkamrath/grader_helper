#create personal access token: https://docs.github.com/en/github/authenticating-to-github/keeping-your-account-and-data-secure/creating-a-personal-access-token
import requests
from github import Github
import re
import os

class GithubHelper:
	def __init__(self, token, organization):
		self.organization = organization
		self.gh = Github(token)
		
	#def Authenticate(self, )

	def GetAllRepos(self, regex=None):
		#r = requests.get('https://github.com/orgs/{}/repos'.format(self.organization), headers={'Authorization': 'token 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'})
		repos = self.gh.get_organization(self.organization).get_repos(type='all')
		if regex:
			regex_filter = re.compile(regex)
			matched = []
			for repo in repos:
				if regex_filter.search(repo.full_name):
					matched.append(repo)
			repos = matched
		return repos

	def CloneRepo(self, repo):
		url = repo.ssh_url
		os.system('git clone {}'.format(url))


if __name__ == '__main__':
	github_helper = GithubHelper('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', "ec-2021-fall")
	org_repos = github_helper.GetAllRepos(".*maps1a*")
	#org_repos = github_helper.GetAllRepos("environment")
	print("num repos: ", len(org_repos))
	for repo in org_repos:
		print(repo)