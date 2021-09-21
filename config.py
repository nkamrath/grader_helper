import datetime
import local_config

"""
The absolute minimum bar for a "config" file
"""
def config_get(key):
    return configs[key]

"""
Necessary configs:
token : your personal access token for GitHub API calls
organization : the name of the organization to query for repos
assignment : the string name of the assignment.  This will be used to regex match the repo names to pull into a workspace
run_unit_tests : if this is set to True, pytest is executed across all repos
due_date : the date time the assignment was due.  This is only used to automatically scan git commits for late submissions (not a perfect method since commit time stamps can be faked)
"""
configs = {
    "token" : local_config.MY_GITHUB_TOKEN,
    "organization" : "ec-2021-fall",
    "assignment" : "maps1b",
    "run_unit_tests" : False,
    "due_date" : datetime.datetime.strptime('2021-09-12 22:00:00', '%Y-%m-%d %H:%M:%S')
}
