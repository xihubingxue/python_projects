# -*- coding: utf-8 -*-

import poplib
from email import parser

imapserver = 'emea.mail.erf.thomson.com'
emailuser = "Qing.Zhang@refinitiv.com"
emailpasswd = "Attorney@198808"

pop_conn = poplib.POP3_SSL(imapserver)
pop_conn.user(emailuser)
pop_conn.pass_(emailpasswd)

# Get messages from server:
messages = [pop_conn.retr(i) for i in range(1, len(pop_conn.list()[1]) + 1)]

# Concat message pieces:
messages = ["\n".join(mssg[1]) for mssg in messages]

# Parse message intom an email object:
messages = [parser.Parser().parsestr(mssg) for mssg in messages]
for message in messages:
    print message['Subject']
pop_conn.quit()