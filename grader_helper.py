from config import config_get
import github_helper
import grader_workspace
import logger
import os

#set this to logger.LOG_LEVEL_INFO to see more verbose output
logger.set_print_level(logger.LOG_LEVEL_ERROR)
logger.log("Assignment {}".format(config_get('assignment')))
logger.log("Gathering repositories...")

#create the github helper with our PAT for github api requests
gh = github_helper.GithubHelper(config_get('token'), config_get('organization'))
#get all repos in the org that match the assignment string regex
repos = gh.get_all_repos('.*{}'.format(config_get('assignment')))

logger.log("repos found in {}: {}".format(config_get('assignment'), len(repos)))
for r in repos:
    logger.log("found repo {} onwer {}".format(r, r.owner))

#setup the workspace for the assignment if it is not already setup and enter it
logger.log('setting up workspace for assignment {}'.format(config_get('assignment')))
workspace = grader_workspace.GraderWorkspace(config_get('assignment'))
workspace.enter_workspace()

#add all git repos from the org query request to the workspace
for r in repos:
    workspace.add_git_repo(r)

#clone/pull everything in the workspace to make sure we are up to date
workspace.clone_all_repos()
mapping, missing = workspace.generate_user_name_mapping()

logger.log("repos missing read to submit: ", missing)
for key, value in mapping.items():
    print("{} -> {}".format(key, value))
logger.log("readyToSubmit count: ", len(mapping))

#run all unit tests if configured
if(config_get("run_unit_tests")):
    workspace.run_all_unit_tests()

#Look for late submissions using the due date and git commit time
for r in repos:
    submission_time = workspace.get_last_commit_time(r)
    due_date = config_get("due_date")
    #print(f"Submission time {submission_time}")
    if(submission_time > due_date):
        print(f"{r.name} was late by \t\t\t\t{submission_time-due_date}")

workspace.exit_workspace()

#logger.log_show()