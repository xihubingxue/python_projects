import email
import imaplib
import re
import sys
import logging
import base64
import email.parser
import html2text
import requests
import json
import argparse

# parser = argparse.ArgumentParser()
# parser.add_argument('-mpass', '-mailbox_password', dest='mailbox_password', help='mailbox password.')
# args = parser.parse_args()

# user = 'Qing.Zhang@refinitiv.com'
# mailbox_password = 'Attorney@198808'
user = 's_quest.user@refinitiv.com'
mailbox_password = 'Packers42-Bears0'
#
# def get_email_body(body):
#     if body.is_multipart():
#         for payload in body.get_payload():
#             print('To:\t\t', body['To'])
#             print('From:\t', body['From'])
#             print('Subject:', body['Subject'])
#             print('Date:\t', body['Date'])
#             for part in body.walk():
#                 if (part.get_content_type() == 'text/plain') and (part.get('Content-Disposition') is None):
#                     output = part.get_payload()
#     else:
#         print('To:\t\t', body['To'])
#         print('From:\t', body['From'])
#         print('Subject:', body['Subject'])
#         print('Date:\t', body['Date'])
#         print('Thread-Index:\t', body['Thread-Index'])
#         text = f"{body.get_payload(decode=True)}"
#         html = text.replace("b'", "")
#         h = html2text.HTML2Text()
#         h.ignore_links = True
#         output = (h.handle(f'''{html}''').replace("\\r\\n", ""))
#         output = output.replace("'", "")
#         # output in one line
#         # output = output.replace('\n'," ")
#         output = output.replace('*', "")
#         return output


def clear_inbox(conn, dest_folder):
    output = []
    result = conn.uid('COPY', emailid, dest_folder)
    output.append(result)
    if result[0] == 'OK':
        result = mov, data = conn.uid('STORE', emailid, '+FLAGS', '(\Deleted Items)')
        conn.expunge()


conn = imaplib.IMAP4_SSL("emea.mail.erf.thomson.com")
conn.login(user, mailbox_password)
conn.select("Inbox")

try:

    resp, items = conn.uid("search", None, 'All')
    items = items[0].split()

    for emailid in items:
        resp, data = conn.uid("fetch", emailid, "(RFC822)")
        if resp == 'OK':
            email_body = data[0][1].decode('utf-8')
            email_message = email.message_from_string(email_body)
            subject = email_message["Subject"]
            if subject.lower().startswith('Darktrace'.lower()):
                #output = get_email_body(email_message)

                # do some task
                # move emails to Processed folder and clear Inbox
                clear_inbox(conn, "Processed")
            else:
                clear_inbox(conn, "backup")

except IndexError:
    print("No new email")

conn.close()
conn.logout()