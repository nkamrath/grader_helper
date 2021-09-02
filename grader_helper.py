from config import config_get
import github_helper
import os
import grader_workspace
import logger

logger.set_print_level(logger.LOG_LEVEL_ERROR)
logger.log("Assaignment {}".format(config_get('assaignment')))
logger.log("Gathering repositories...")

gh = github_helper.GithubHelper(config_get('token'), config_get('organization'))
repos = gh.GetAllRepos('.*{}'.format(config_get('assaignment')))

logger.log("repos found in {}: {}".format(config_get('assaignment'), len(repos)))
for r in repos:
	logger.log("found repo {} onwer {}".format(r, r.owner))

# print("clone url: ", repos[0].ssh_url)
# gh.CloneRepo(repos[0])

logger.log('setting up workspace for assaignment {}'.format(config_get('assaignment')))
workspace = grader_workspace.GraderWorkspace(config_get('assaignment'))
workspace.enter_workspace()

for r in repos: workspace.clone_repo(r)

mapping, missing = workspace.generate_user_name_mapping()

print("missing: ", missing)
#print(mapping)
for key, value in mapping.items():
	print("{} -> {}".format(key, value))
print("student count: ", len(mapping))

workspace.exit_workspace()

#logger.log_show()