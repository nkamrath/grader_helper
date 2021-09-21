import datetime
from itertools import product
import logger
from multiprocessing import Pool
import os
import re
import subprocess

'''
The GraderWorkspace object is a logical management unit which provides a clean way to segment grading space for an assignment.
It facilitates the setup and management of on disk repos.  The workspace is essentally a root directory for pulling repos into.
Once repos are added, they can easily be pulled and inspected for readyToSubmit files, commit date/times, and running unit tests.
Any code that provides functionality for interacting with repos on disk should be added here.
'''
class GraderWorkspace:
    def __init__(self, assignment):
        self.assignment = assignment
        self.name = self.assignment + '-workspace'
        self.root_path = os.getcwd()
        self.repos = []

        if(not os.path.exists(self.name)):
            os.mkdir(self.name)

    '''
    Change directory to the root of the workspace
    '''
    def enter_workspace(self):
        os.chdir(self.root_path)
        os.chdir(self.name)

    '''
    Change directory to just above the root of the workspace
    '''
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

    '''
    Clone the specified repo.  uses system shell for git clone command.
    If the repo was already found on disk, attemps to pull the repo to find any updates
    '''
    def clone_repo(self, repo):
        self.add_git_repo(repo)
        if(not os.path.exists(repo.name)):
            url = repo.ssh_url
            os.system('git clone {}'.format(url))
        else:
            logger.log('repository {} already found, skipped clone'.format(repo.full_name))
            os.chdir(repo.name)
            os.system('git pull')
            os.chdir('..')

    '''
    Attempts to clone all repos in the workspace using a process pool.
    If the repo was already on disk, a pull is attempted instead to fetch updates.
    '''
    def clone_all_repos(self, process_pool_size=4):
        logger.log('cloning all repos')
        self.enter_workspace()
        proc_args = [(self, x) for x in self.repos]

        #careful here, doing too many parallel pulls makes GitHub angry.  They have a limit to API and SSH actions even for Pro users.
        with Pool(process_pool_size) as pool:
            pool.starmap(GraderWorkspace.clone_repo, proc_args)
        logger.log('done')

    '''
    Attempt to run the unit tests for the specified repo and place the output into the specified text file.
    '''
    def run_unit_tests(self, repo, test_output_file='unit_test_results.txt'):
        if(os.path.exists(repo.name)):
            os.chdir(repo.name)
            os.system(f'pytest > {test_output_file}')
            os.chdir('..')
        else:
            print(f'Error repo {repo} not on disk')

    '''
    Attempt to run unit tests for every repo in the workspace using a process pool.
    '''
    def run_all_unit_tests(self, process_pool_size=8):
        logger.log('running all unit tests...')
        self.enter_workspace()
        proc_args = [(self, x) for x in self.repos]
        with Pool(process_pool_size) as pool:
            pool.starmap(GraderWorkspace.run_unit_tests, proc_args)

        logger.log('done')

    '''
    Get the last commit time for the specified repo as a python date time object.
    '''
    def get_last_commit_time(self, repo):
        os.chdir(repo.name)
        #we parse the results of a git log on the latest commit and use a regex to get only the date-time componenets from the result.
        p = subprocess.Popen(['git', 'log' , '-1', '--date=iso'], stdout=subprocess.PIPE)
        out, err = p.communicate()
        m = re.search('\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}', str(out))
        os.chdir('..')
        date_time = datetime.datetime.strptime(m.group(0), '%Y-%m-%d %H:%M:%S')
        return date_time

    '''
    Generate a GitHub user name to auburn student ID mapping using the readyToSubmit.txt files where available.
    Returns the mapping as tuples but also a list of missing users (repos with no readToSubmit.txt)
    '''
    def generate_user_name_mapping(self):
        #we have to look through every git repo that we know of and check the readyToSubmit.txt
        logger.log('Checking readyToSubmit.txt to build user name mappings...')
        self.enter_workspace()
        user_mapping = {}
        missing = []
        for repo in self.repos:
            #try to clone the repo just in case it isn't pulled down
            #look for ready to submit
            ready_path = os.path.join(repo.name, 'readyToSubmit.txt')
            if(os.path.exists(repo.name) and os.path.exists(ready_path)):
                au_user = 'None'
                with open(ready_path) as f:
                    lines = f.readlines()
                    if(len(lines) == 1):
                        au_user = lines[0]
                    elif(len(lines)==2):
                        au_user = lines[1]
                    else:
                        au_user = 'MISSING!!!'
                    au_user = au_user.strip()
                git_user = repo.name[len(self.assignment)+1:]
                logger.log('found user in ready to submit: {} -> {}'.format(au_user, git_user))
                user_mapping[git_user] = au_user
            else:
                logger.log('no ready to submit in {}'.format(repo.name), logger.LOG_LEVEL_WARNING)
                missing.append(repo.name[len(self.assignment)+1:])

        logger.log('user mapping: {}'.format(user_mapping))
        return user_mapping, missing
