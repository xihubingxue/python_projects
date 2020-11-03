#coding:utf-8
import imaplib, email, os
import email.mime
imapserver = 'imap.163.com'
#imapserver = 'outlook.office365.com         '
emailuser = "zhang.qing.happy@163.com"
#emailuser = "s_quest.user@refinitiv.com"
emailpasswd = "WHHSWVTTFADSXYYU"
#emailpasswd = "Packers42-Bears0"


attachementdir = r"d:\a"  # 附件存放的位置

imaplib.Commands['ID'] = ('AUTH')
conn = imaplib.IMAP4_SSL(imapserver, 993)
conn.login(emailuser, emailpasswd)

# 上传客户端身份信息
args = ("name","catherine","contact",emailuser,"version","1.0.0","vendor","myclient")
typ, dat = conn._simple_command('ID', '("' + '" "'.join(args) + '")')
print(conn._untagged_response(typ, dat, 'ID'))


#conn.list()  # 列出邮箱中所有的列表，如：收件箱、垃圾箱、草稿箱。。。

res=conn.select('INBOX')  # 选择收件箱（默认）


result, dataid = conn.search(None, "ALL")

mailidlist = dataid[0].split()  # 转成标准列表,获得所有邮件的ID


# 解析邮件内容
def get_body(msg):
    if msg.is_multipart():
        return get_body(msg.get_payload(0))
    else:
        return msg.get_payload(None, decode=True)


# search('FROM','abc@outlook.com',conn)  根据输入的条件查找特定的邮件
def search(key, value, conn):
    result, data = conn.search(None, key, '"()"'.format(value))
    return data


# 获取附件
def get_attachements(msg):
    for part in msg.walk():
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue
        filename = part.get_filename()

        if bool(filename):
            filepath = os.path.join(attachementdir, filename)
            with open(filepath, 'wb') as f:
                f.write(part.get_payload(decode=True))


for id in mailidlist:
    result, data = conn.fetch(id, '(RFC822)')  # 通过邮件id获取邮件
    e = email.message_from_bytes(data[0][1])
    subject = email.header.make_header(email.header.decode_header(e['SUBJECT']))
    mail_from = email.header.make_header(email.header.decode_header(e['From']))
    if "Apple" in subject._chunks[0][0]:
        print("邮件的subject是%s" % subject)
        print("邮件的发件人是%s" % mail_from)
        body = str(get_body(e), encoding='utf-8')  # utf-8 gb2312 GB18030解析中文日文英文
        print("邮件内容是%s" % body)

conn.logout()

