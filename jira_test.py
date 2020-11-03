# coding=UTF-8
from __future__ import unicode_literals
from lib.jira_api import *
from send_email import initlog, send_mail_to_user



def create_sub_task(fields):

    # get the value of fields from form
    email_title = fields["email_title"]

    # Search email by title
    # email_a = email_api()
    # email_list = email_a.get_messages_by_subject_date(subject=email_title)
    # email_info = ""
    # for email in email_list:
    #     email_info = email["bodyPreview"]
    email_info = email_title

    #close_flag = fields["close"]

    parent_number = fields["parent"]

    user_name = fields["user_name"]

    logger.debug("Email tile is {}".format(email_title).encode('utf-8'))
    logger.debug("The name of the user is {}".format(user_name))
    logger.debug("The number of parent ticket is {}".format(parent_number))

    jira_o = jira_api()

    jira_client = jira_o.jiraClient

    parent_issue = jira_client.issue(parent_number)

    user = jira_client.user(user_name)

    # sub_issue = jira_client.create_issue(parent={'key': parent_issue}, project=parent_issue.fields.project,
    #                                      summary='New issue from jira-python',
    #                                      description='Look into this one', issuetype={'name': 'Bug'})
    # for number in ['QRP-5781', 'QRP-5782','QRP-5780']:
    #     transitions = jira_client.transitions(number)
    #     status = [(t['id'], t['name']) for t in transitions]
    #     print ("The statuses are {}".format(status))

    # close sub tickets before modifying it
    #issue.fields.components[0].name
    #try:
    # if close_flag == "1":
    #     count_sub_closed = jira_o.close_sub_tasks(parent_issue)
    #     logger.debug("Have closed {} sub tasks".format(count_sub_closed))

    #custom_field_map = jira_o.get_customFieldMap()

    #search parent ticket
    #parent_issue = jira_o.get_QRP_parent_issue(custom_field_map, parent_number)

    sub_task_dic = jira_o.get_subtask_fields(parent_issue, email_info,
                                             others={"user_name": user_name, "email_title": email_title})

    sub_issue = jira_client.create_issue(fields=sub_task_dic)

    # Start Progress for the new created task
    jira_client.transition_issue(sub_issue, jira_o.special_status['Start Progress'],
                                     comment='change the status automatically')

    if sub_issue:
        logger.debug('the subtask {} has been created successfully'.format(sub_issue.key))

    # Start to send the link of subtak in an email to the user
    logger.debug("Start to mail the link of subtak  to the user")
    
    logger2 = initlog()
    
    send_mail_to_user('https://jira.refinitiv.com/browse/' + sub_issue.key, logger2, email=user.emailAddress)

    return sub_issue.key


if __name__ == "__main__":
    create_sub_task()




