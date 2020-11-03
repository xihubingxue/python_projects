import requests

from lib.jira_api import logger


class email_api(object):
    def __init__(self):
        self.rest_api = " https://graph.microsoft.com/v1.0/"
        self.token = "c19xdWVzdC51c2VyOlBhY2tlcnM0Mi1CZWFyczA="

    def get_messages_by_subject_date(self, subject=None, start_time=None, end_time=None):
        logger.info("get all your messages")
        if subject== None and start_time== None and end_time== None:
            filter= ""
        else:
            filter = "$filter="
            if start_time is not None:
                filter= filter + "receivedDateTime ge "+start_time
            if end_time is not None:
                filter = filter + "and receivedDateTime lt "+end_time
            if subject is not None:
                filter = filter + "and subject eq " + subject
            #bodyPreview, body
        r = requests.get(self.rest_api + "me/messages?" + filter, headers={'Authorization': 'Bearer ' + self.token})
        logger.info(r.text)
        return r.json()

    def fuzzy_query_messages_by_subject_date(self, subject=None, start_time=None, end_time=None):
        logger.info("get all your messages")
        if start_time == None and end_time == None:
            filter = ""
        else:
            filter = "$filter="
            if start_time is not None:
                filter = filter + "receivedDateTime ge " + start_time
            if end_time is not None:
                filter = filter + "and receivedDateTime lt " + end_time
            # bodyPreview, body
        r = requests.get(self.rest_api + "me/messages?" + filter, headers={'Authorization': 'Bearer ' + self.token})
        logger.info(r.text)
        filtered_msg_list = []
        if subject is not None:
            filtered_msg_list = self.filter_messages_by_subject(subject=subject)

        return filtered_msg_list

    def filter_messages_by_subject(self, subject=None, message_list=[]):
        filtered_msg_list = []
        if message_list.__len__() > 0:
            for message in message_list:
                if subject is not None and subject in message['subject']:
                    filtered_msg_list.append(message["subject"])
        return filtered_msg_list

