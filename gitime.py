#!/usr/bin/python

import sys
import requests
import os

try:
    from settings import *
except:
    raise ImportError("You need a settings file")

# Borrowed from https://stackoverflow.com/a/56787591

updated_after = "2020-01-01T00:00:00.00Z"
updated_before = "2020-03-01T00:00:00.00Z"

def get_project_hours(project_id, _from, _to):
    item_counter = 0
    total_seconds = 0
    
    headers = { 'Private-Token': ACCESS_TOKEN }
    url_template = "{base_url}/projects/{project_id}/issues?" \
                   "&updated_after={updated_after}&updated_before={updated_before}"
    url = url_template.format(base_url=BASE_URL, project_id=project_id, username=USERNAME,
                              updated_after=updated_after, updated_before=updated_before)
    
    # call API
    issues = requests.get(url, headers = headers)
    
    total_seconds = 0
    issues_to_pay = []
    line_template = "id: {id}    time spent: {time}\ttitle: {title}\turl: {url}"
    print("Issue statistics for {u} from {f} to {t}:\n".format(u=USERNAME,f=updated_after, t=updated_before))
    
    for issue in issues.json():
    
        time_val = issue['time_stats']['human_total_time_spent']
        already_paid = u'paid' in issue['labels'] # you can put a label 'paid' to exclude an issue
        if already_paid:
            time_val = time_val + " *"
        else:
            # if the issue has been paid, already, don't add the time, and don't list as to be paid
            total_seconds += issue['time_stats']['total_time_spent']
            issues_to_pay.append(str(issue['id']))
    
        line = line_template.format(
            id=issue['id'],
            title=issue['title'],
            time=time_val,
            url=issue['web_url']
        )
        if time_val != None: print(line)
    total_hours = float((float(total_seconds) / 60) / 60)
    print("")
    print("Hours to pay on all issues: %.2f" % total_hours)
    print("")
    print("* = issue has been paid for, already")
    print("All issue to pay: {issues}".format(issues=",".join(issues_to_pay)))
    return total_hours

if __name__ == '__main__':
    total_hours = 0
    for project_id in sys.argv[1:]:
        print("\n...")
        print("*** Stats for project: project_id".format(project_id))
        total_hours += get_project_hours(project_id, updated_after, updated_before)

    print("")
    print("*** Total hours among all projects %.2f" % (total_hours))
