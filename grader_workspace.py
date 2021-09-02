import os
import logger

class GraderWorkspace:
	def __init__(self, assaignment):
		self.assaignment = assaignment
		self.name = self.assaignment + '-workspace'
		self.root_path = os.getcwd()
		self.repos = []

		if(not os.path.exists(self.name)):
			os.mkdir(self.name)

	def enter_workspace(self):
		os.chdir(self.root_path)
		os.chdir(self.name)

	def exit_workspace(self):
		os.chdir(self.root_path)

	def add_git_repo(self, repo):
		exists = False
		for known_repo in self.repos:
			if(known_repo.full_name == repo.full_name):
				exists = True
				break

		if not exists:
			self.repos.append(repo)

	def clone_repo(self, repo):
		self.add_git_repo(repo)
		if(not os.path.exists(repo.name)):
			url = repo.ssh_url
			os.system('git clone {}'.format(url))
		else:
			logger.log("repository {} already found, skipped clone".format(repo.full_name))

	def clone_all_repos(self):
		self.enter_workspace()
		for repo in self.repos:
			self.clone_repo(repo)

	def generate_user_name_mapping(self):
		#we have to look through every git repo that we know of and check the readyToSubmit.txt
		logger.log("Checking readyToSubmit.txt to build user name mappings...")
		self.enter_workspace()
		user_mapping = {}
		missing = []
		for repo in self.repos:
			#try to clone the repo just in case it isn't pulled down
			self.clone_repo(repo)
			#look for ready to submit
			ready_path = os.path.join(repo.name, "readyToSubmit.txt")
			if(os.path.exists(repo.name) and os.path.exists(ready_path)):
				au_user = "None"
				with open(ready_path) as f:
					lines = f.readlines()
					if(len(lines) == 1):
						au_user = lines[0]
					elif(len(lines)==2):
						au_user = lines[1]
					else:
						au_user = "MISSING!!!"
					au_user = au_user.strip()
				git_user = repo.name[len(self.assaignment)+1:]
				logger.log("found user in ready to submit: {} -> {}".format(au_user, git_user))
				user_mapping[git_user] = au_user
			else:
				logger.log("no ready to submit in {}".format(repo.name), logger.LOG_LEVEL_WARNING)
				missing.append(repo.name[len(self.assaignment)+1:])

		logger.log("user mapping: {}".format(user_mapping))
		return user_mapping, missing
