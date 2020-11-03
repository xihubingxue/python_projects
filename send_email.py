import email
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import re
import time
import sys
import subprocess
import logging
import logging.handlers
import socket
import smtplib

import resp


class MailCreator:
    def __init__(self):
        self.msg = email.message.Message()
        self.mail = ""
        
    def create(self, mailheader, maildata, mailattachlist=[]):
        if not mailheader or not maildata:
            return
        char_set = 'utf-8'
        for k in mailheader.keys():
            if k == 'subject':
                self.msg[k] = email.header.Header(mailheader[k], char_set)
            else:
                self.msg[k] = mailheader[k]
     
        body_plain = MIMEText(maildata[0], _subtype='html', _charset=char_set)
        body_html = None

        if maildata[1]:
            body_html = MIMEText(maildata[1], _subtype='html', _charset=char_set)
        
        attach=MIMEMultipart()
        attach.attach(body_plain)
        if body_html:
            attach.attach(body_html)
            
        for fname in mailattachlist:
            attachment=MIMEText(email.Encoders._bencode(open(fname,'rb').read()))
            attachment.replace_header('Content-type','Application/octet-stream;name="'+os.path.basename(fname)+'"')
            attachment.replace_header('Content-Transfer-Encoding', 'base64')
            attachment.add_header('Content-Disposition','attachment;filename="'+os.path.basename(fname)+'"')
            attach.attach(attachment)
           
        self.mail = self.msg.as_string()[:-1] + attach.as_string()
        
        return self.mail


def initlog():  
    logger = logging.getLogger('GATSMonitorLog')
    LOG_FILENAME = 'GATSMonitor.log'
    handler = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes = 10000000, backupCount = 5)
    formatter = logging.Formatter('%(asctime)s %(levelname)-6s %(message)s', '%d%b %H:%M:%S',)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    return logger


def _send_mail(to_list,mail):  
    fromaddr = 'not_reply@thomsonreuters.com'  
    toaddr = ";".join(to_list)
    res = None
    try:
        s = smtplib.SMTP('mailhub.tfn.com')
        code = s.ehlo()[0]
        if not (200 <= code <=299):
            usesesntp = 0
            code = s.helo()[0]
            if not (200 <= code <=299):
                raise smtplib.SMTPHeloError(code, resp)
        res=s.sendmail(fromaddr,toaddr,mail)
    except(socket.gaierror,socket.error,socket.herror,smtplib.SMTPException) as e:

        print ("**ERROR**Your message may not have been sent!")
        return 1
    else:
        print ("***Message successful sent to %d recipient(s)" % len(to_list))
        return 0


def send_mail_to_user(content,logger, email='Qing.Zhang@refinitiv.com'):
    allmailbody = '<html>\n<body>\n<body>\n<table border="0" width="100%%">\n<tr>\n<td width="100%%" align="left">Your sub task created successfully</td>\n</tr>\n'
    allmailbody = allmailbody + '<tr>\n<td width="100%%" align="left"></td>\n</tr>'
    allmailbody = allmailbody + '<br\>\n<tr>\n<td width="100%%" align="left">Hi '+ email.split(".")[0] +',</td>\n</tr>\n<tr>\n<td width="100%%" align="left"></td>\n</tr>\n'
    allmailbody = allmailbody+'<tr>\n<td width="100%%" align="left">You just created a new sub task of QRP, please refer to '+content+' for detail</td>\n</tr>\n</table>\n</body>\n</html>\n'
    mc = MailCreator()
    toList = [email]
    header = {'from': 'not_reply@thomsonreuters.com', 'to':';'.join(toList), 'subject':'Your new sub task'}
    print ('header of email: %s'%header)
    mail = mc.create(header, [allmailbody, ''])
    logger.info('prepared email ok')
    res = _send_mail(toList, mail)
    if res != 0:
        logger.error('**ERROR**Your message may not have been sent!')
        logger.error(allmailbody)
    else:
        logger.info('**EMAIL sent out**!')
    

if __name__ == "__main__":
    version = '1.0'
    logger = initlog()
    send_mail_to_user('https://jira.refinitiv.com/browse/QRP-5769', logger)
    