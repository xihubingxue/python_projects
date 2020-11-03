#!/usr/bin/env python
# coding:utf-8
import json
import os.path
from datetime import datetime, date, timedelta, time

import tornado.web
from tornado.options import define, options

from jira_test import create_sub_task
from lib import db_operation
from lib.email_api import *
from lib.jira_api import *


define("port", default=9999, help="run on the given port", type=int)
class IndexHandler(tornado.web.RequestHandler):
  def get(self):
    """
    load users from json file and then send to page to display as testers
    fetch release emails in the past week and get the email titles to display as Release

    :return:
    """
    users = db_operation.get_users()
    email_a = email_api()
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (date.today() + timedelta(days=-6)).strftime("%Y-%m-%d")
    logger.debug("start_date is {}".format(start_date))
    logger.debug("end_date is {}".format(end_date))
    release_mails = email_a.fuzzy_query_messages_by_subject_date(subject="", start_time=start_date, end_time=end_date)
    release_mails = ["Elektron – Windows Collections Head End CHE_HKS_2.01.00.02 Software Release", "TDCHE_SGE_CZCE_CFFEX_DCE Release 0.3.16-0 is ready for QuEST qualification"]
    self.render("static/create_sub_task.html", path=os.path.split(os.path.realpath(__file__))[0].replace('\\', '/'),
                users=json.dumps(users), mails=json.dumps(release_mails))


class TaskHandler(tornado.web.RequestHandler):
  def get(self):

    email_title = self.get_argument("emailTitle")
    parent = self.get_argument("parent")
    user_name = self.get_argument("userName")
    fields = {"email_title": email_title, "parent": parent, "user_name": user_name}
    sub_task_dict = dict()
    jira_o = jira_api()
    jira_client = jira_o.jiraClient
    if email_title:
      sub_task_key = create_sub_task(fields)
      #sub_task_key = "QRP-5780"
      sub_task_dict.update({"key": sub_task_key})
      sub_task_dict.update({"link": jira_o.JiraTicketUrl + sub_task_key})
      self.write(json.dumps(sub_task_dict))


class LoadHandler(tornado.web.RequestHandler):
  def get(self, *args, **kwargs):

    parent = self.get_argument("parent")

    jira_o = jira_api()
    jira_client = jira_o.jiraClient
    parent_issue = jira_client.issue(parent)

    sub_tasks = parent_issue.fields.subtasks

    sub_task_dict = dict()

    for sub_task in sub_tasks:
      if sub_task.fields.status.name != "Closed":
        sub_task_dict.update({sub_task.key: sub_task.fields.summary})

    logger.debug("sub tasks that are not closed are ===={}".format(sub_task_dict))

    self.write(json.dumps(sub_task_dict))


class CloseHandler(tornado.web.RequestHandler):
  def get(self, *args, **kwargs):

    selected_tasks = self.get_argument("selected_task")

    if selected_tasks:
      selected_tasks=selected_tasks.split(",")

    parent = self.get_argument("parent")

    jira_o = jira_api()

    jira_client = jira_o.jiraClient

    sub_issues = []
    for sub_issue in selected_tasks:
      sub_issues.append(jira_client.issue(sub_issue))

    count_sub_closed = jira_o.close_sub_tasks(sub_issues)

    logger.info("Have closed {} sub tasks".format(count_sub_closed))

    parent_issue = jira_client.issue(parent)

    sub_tasks = parent_issue.fields.subtasks

    sub_task_dict = dict()

    sub_task_dict.update({"closed": [sub_issue.key for sub_issue in sub_issues]})

    for sub_task in sub_tasks:
      if sub_task.fields.status.name != "Closed":
        sub_task_dict.update({sub_task.key: sub_task.fields.summary})

    self.write(json.dumps(sub_task_dict))


handlers = [
  (r"/", IndexHandler),
  (r"/task", TaskHandler),
  (r"/load", LoadHandler),
  (r"/close", CloseHandler)
]


#static_path = os.path.join(os.path.dirname(__file__), "static")

if __name__ == "__main__":
  tornado.options.parse_command_line()
  app = tornado.web.Application(handlers, static_path=os.path.join(os.path.dirname(__file__), "static"))
  http_server = tornado.httpserver.HTTPServer(app)
  http_server.listen(options.port)
  tornado.ioloop.IOLoop.instance().start()