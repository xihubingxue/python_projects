# coding:utf-8
import pprint
from base64 import b64decode

import requests
from jira import JIRA
from log_manager import Log
logger = Log().logger


class jira_api(object):
    def __init__(self):
        # self.server = 'https://jira.refinitiv.com/'
        # # b64 encoding of string with form 'username:password'
        self.auth = 'UWluZy5aaGFuZzpBdHRvcm5leUAxOTg4MDg='
        # #self.username, self.password = b64decode(bytes(self.auth, 'UTF-8')).split(':')
        # self.username, self.password= "Qing.Zhang@refinitiv.com" , "Attorney@198808"
        # self.jiraClient = JIRA(server=self.server, basic_auth=(self.username, self.password))
        JiraHome = 'https://jira.refinitiv.com'
        self.JiraTicketUrl = 'https://jira.refinitiv.com/browse/'
        # b64 encoding of string with form 'username:password'
        self.auth = 'c19xdWVzdC51c2VyOlBhY2tlcnM0Mi1CZWFyczA='
        user, pw = b64decode(self.auth).split(':')
        #user,pw = "Qing.Zhang@refinitiv.com", "Attorney@198808"
        self.jiraClient = JIRA(JiraHome, basic_auth=(user, pw))
        self.special_status = {'Start Progress': '71',  'Close': '81'}
        self.rest_api = "https://jira.refinitiv.com/rest/api/2/"
        # projects = self.jiraClient.projects()
        # for project in projects:
        #     if project.key == "APAC":
        #         print("project is ===={}".format(project))
        # print ("projects are ======{}".format(projects))
        # fields = self.jiraClient.fields()
        # issue = self.jiraClient.issue('QRP-5769')

        # url = 'https://jira.refinitiv.com/rest/gadget/1.0/login'
        # auth = {
        #     "os_username": self.username,
        #     "os_password": self.password,
        #     "os_cookie": "true",
        #     "os_captcha": ""
        # }
        # session = requests.session()
        # res=session.post(url, auth)
        # # jira的高级查询sql
        # today_deploy_plan = 'project = "Quest Release Project"'
        # payload = {
        #     "jql": today_deploy_plan,
        #     # 根据判断条件取出的条数，默认是取300-400之间
        #     'maxResults': 5000
        # }
        # uri = "http://jira.refinitiv.com/rest/api/2/project"
        # rep = session.get(uri)

        #self.jiraClient = JIRA(auth=(self.username, self.password), options={'server': self.server})

    def transite_issues(self, issues):
        pass

    def in_status(self,  status, f='Close'):
        for s in status:
            if f in s:
                return True

    def get_subtask_fields(self,  parent, summary, others=None):
        user_name = ""
        email_title = ""
        customFieldMap = self.get_customFieldMap()
        epic = self.jiraClient.issue(parent.fields.customfield_10236)
        if others is not None:
            if "user_name" in others:
                user_name = others["user_name"]
            if "email_title" in others:
                email_title = others["email_title"]
        sub_task_fields = {
                           'parent': {'key': parent.key},
                           'project': {'key': 'QRP'},
                           'assignee': {'name': user_name},
                           'issuetype': {'name': 'Sub-task'},
                           'summary': email_title + ' test',
                           'priority': {'id': epic.fields.priority.id},
                           'components': [{'name': parent.fields.components[0].name}],
                           'description': summary,
                        #    'reporter': parent.fields.reporter.name
                        #'labels': [parent.fields.labels[0]],
                        #customFieldMap['Geographic Region']: [{'value': parent.fields.
                        #    customfield_11754[0].value}],
                        #     [{'value': region} for region in parent.fields.region],
                        # customFieldMap['Target start']: parent.fields[customFieldMap['Integration Start Date']],
                        # customFieldMap['Target end']: parent.fields[customFieldMap['Integration Signoff']],
                        #customFieldMap['Release Type']: {'value': parent.fields.customfield_12446.value},
                        #customFieldMap['Workstream']: {'value': parent.fields.customfield_11756.value},
                        customFieldMap['Sub-task Category']: None
                        }

        return sub_task_fields

    def get_customFieldMap(self):
        """
        Get the mapping of visible field name to Jira custom field ids.
        The list of fields to retrieve is hard coded here.  Update this list if a new field is needed.

        Returns: a dictionary with the mapping of visible field name to Jira custom field id
        """
        customFieldMap = {
            'Collections Squad': None,
            'Development Owner': None,
            'Driver/s': None,
            'Delivery Date': None,
            'Epic Link': None,
            'Integration Start Date': None,
            'Integration Signoff': None,
            'Geographic Region': None,
            'Live Date': None,
            'RAG Status Comment': None,
            'Release Type': None,
            'Target end': None,
            'Target Platform': None,
            'Target start': None,
            'Workstream': None,
            'Sub-task Category': None,
            'Team': None
        }
        result = self.jiraClient.fields()
        if not result:
            logger.error('No updates will be done.  Cannot get JIRA custom field info.')
            exit(1)
        for fieldInfo in result:
            fieldName = fieldInfo['name']
            if fieldName in customFieldMap:
                customFieldMap[fieldName] = fieldInfo['id']
        logger.debug('customFieldMap:\n' + pprint.pformat(customFieldMap))
        return customFieldMap

    def get_QRP_parent_issue(self, customFieldMap, key):
        """
        Get infomation on QRP 'Release' issues matching criteria:
        key = key

        Arguments:
            customFieldMap : a mapping of visible field names to JIRA internal custom field id
                             use get_customFieldMap() to get this mapping

        Returns JSON object with the query results.

        """
        fieldList = 'key,components,issuelinks,status,summary' \
                    + ',' + customFieldMap['Epic Link'] \
                    + ',' + customFieldMap['RAG Status Comment'] \
                    + ',' + customFieldMap['Target start'] \
                    + ',' + customFieldMap['Target end'] \
                    + ',' + customFieldMap['Geographic Region'] \
                    + ',' + customFieldMap['Release Type'] \
                    + ',' + customFieldMap['Collections Squad']
        query = 'key = ' + key
        try:
         result = self.jiraClient.search_issues(jql_str=query, maxResults=1000, fields=fieldList, json_result=True)
        except Exception as e:
         print(e)
        if not result:
            logger.error('Cannot get QRP issues from JIRA.')
            exit(1)
        return result.get('issues', {})

    # def close_sub_tasks(self, parent_issue):
    #     logger.debug("Start to close sub tasks")
    #     count_sub_closed = 0
    #     for issue in parent_issue.fields.subtasks:
    #         # the issue is not closed
    #         if issue.fields.status.name != 'Closed':
    #             count_sub_closed += 1
    #             transitions = self.jiraClient.transitions(str(issue.key))
    #             status = [(t['id'], t['name']) for t in transitions]
    #             # the status contains 'Close'
    #             try:
    #                 if self.in_status(status):
    #                     self.jiraClient.transition_issue(issue, self.special_status['Close'],
    #                                                      comment='change the status automatically')
    #
    #                 # the status doesn't contain 'Close'
    #                 else:
    #                     # the status contain 'Start Progress'
    #                     if self.in_status(status, f='Start Progress'):
    #                         # should firstly transit to 'Start Progress', then transit to 'Close'
    #                         self.jiraClient.transition_issue(issue, self.special_status['Start Progress'],
    #                                                      comment='change the status automatically')
    #                         self.jiraClient.transition_issue(issue, self.special_status['Close'],
    #                                                      comment='change the status automatically')
    #             except Exception as e:
    #                     count_sub_closed-=1
    #                     logger.debug("Fail to close sub task {}".format(str(issue.key)))
    #                     return
    #             # issue_temp.update(summary="Closed The second sub task for testing jira tool. Please don't use it.")
    #     return count_sub_closed

    def close_sub_tasks(self, sub_tasks):
        count_sub_closed = 0
        for task in sub_tasks:
            count_sub_closed += 1
            transitions = self.jiraClient.transitions(str(task.key))
            status = [(t['id'], t['name']) for t in transitions]
            # the status contains 'Close'
            try:
                if self.in_status(status):
                    self.jiraClient.transition_issue(task, self.special_status['Close'],
                                                     comment='change the status automatically')

                # the status doesn't contain 'Close'
                else:
                    # the status contain 'Start Progress'
                    if self.in_status(status, f='Start Progress'):
                        # should firstly transit to 'Start Progress', then transit to 'Close'
                        self.jiraClient.transition_issue(task, self.special_status['Start Progress'],
                                                         comment='change the status automatically')
                        self.jiraClient.transition_issue(task, self.special_status['Close'],
                                                         comment='change the status automatically')
            except Exception as e:
                count_sub_closed -= 1
                logger.debug("Fail to close sub task {}".format(str(task.key)))
                return
            # issue_temp.update(summary="Closed The second sub task for testing jira tool. Please don't use it.")
        return count_sub_closed

    def get_user_by_username(self, user_name):
        logger.info("get user by user name")
        r = requests.get(self.rest_api + "user?username=" + user_name, headers={'Authorization': 'Basic ' + self.auth,
                                                                                'Content-Type': 'application/json'})
        logger.info(r.text)
        return r.json()
