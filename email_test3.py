import datetime
from exchangelib import (
    Credentials,
    Account,
    DELEGATE,
    Configuration,
    FileAttachment,
    EWSDateTime,
    EWSTimeZone,
)
from exchangelib.protocol import CachingProtocol


class EmailLoader:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.account = self.connect_to_mailbox()

    def connect_to_mailbox(self):
        cred = Credentials(self.username, self.password)
        config = Configuration(server="emea.mail.erf.thomson.com", credentials=cred,)
        account = Account(
            primary_smtp_address=self.username,
            config=config,
            autodiscover=False,
            access_type=DELEGATE,
        )
        print("--------Connected--------")
        return account

    def get_email_list(self, send_time_gte, subject_like=None, sender=None):
        """

        :param send_time_gte: must be specified
        :param subject_like: if None, it means no restrictions
        :param sender: if None, it means no restrictions
        :return: list type
        """
        tz = EWSTimeZone.timezone("Asia/Shanghai")
        email_list = []
        send_time_gte = datetime.datetime.strptime(send_time_gte, "%Y-%m-%d")
        # inbox = self.account.inbox.filter(
        #     datetime_sent__gte=tz.localize(
        #         EWSDateTime(send_time_gte.year, send_time_gte.month, send_time_gte.day)
        #     )
        # )

        for item in self.account.inbox.all().order_by("-datetime_sent"):
            subject = item.subject
            if not item.sender:
                continue
            sender_name = item.sender.name
            send_time = (item.datetime_sent + datetime.timedelta(hours=8)).strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            b1 = (
                True
                if not subject_like or subject_like.lower() in subject.lower()
                else False
            )
            b2 = True if not sender or sender.lower() in sender_name.lower() else False

            if b1 and b2:
                email_list.append([subject, sender_name, send_time])
        print("get {} email(s) in total".format(len(email_list)))
        return email_list

    def download_email(self, subject, sender, send_time):
        """
        all three parameters must be specified
        only download one email each time
        :param subject:
        :param sender:
        :param send_time:
        :return: dict type
        """
        tz = EWSTimeZone.timezone("UTC")
        _dict = {}
        send_time = datetime.datetime.strptime(
            send_time, "%Y-%m-%d %H:%M:%S"
        ) - datetime.timedelta(hours=8)
        send_time = tz.localize(
            EWSDateTime(
                send_time.year,
                send_time.month,
                send_time.day,
                send_time.hour,
                send_time.minute,
                send_time.second,
            )
        )
        inbox = (
            self.account.inbox.filter(datetime_sent__gte=send_time,)
            .filter(datetime_sent__lte=send_time)
            .filter(subject__icontains=subject)
        )

        for item in inbox.all().order_by("-datetime_sent"):
            if sender.lower() in item.sender.name.lower():
                _dict["content"] = item.text_body
                _dict["attachments"] = [
                    {"name": attachment.name, "content": attachment.content}
                    for attachment in item.attachments
                    if isinstance(attachment, FileAttachment)
                ]
                if _dict:
                    print('one mail meets conditions')
                return _dict
            return

    @staticmethod
    def close_connections():
        CachingProtocol.clear_cache()


emailLoader = EmailLoader(username="Qing.Zhang@refinitiv.com", password="Attorney@198808")
email_list = emailLoader.get_email_list(send_time_gte="2020-03-10")
print(email_list[0][2])  # latest mail sent-time
print(email_list[-1][2])  # oldest mail sent-time
latest_mail = emailLoader.download_email(
    email_list[0][0], email_list[0][1], email_list[0][2]
)
oldest_mail = emailLoader.download_email(
    email_list[-1][0], email_list[-1][1], email_list[-1][2]
)
emailLoader.close_connections()