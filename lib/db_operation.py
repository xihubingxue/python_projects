import json
import os
import sqlite3
from collections import OrderedDict
from random import randint
template_path = os.path.split(os.path.realpath(__file__))[0].replace('\\', '/')

def connect_db():
    conn = sqlite3.connect('jira_tool')
    cursor = conn.cursor()
    print ("Opened database successfully")
    return conn, cursor


def create_table():
    conn, cursor = connect_db()
    cursor.execute('''CREATE TABLE JIRAUSER (ID INT PRIMARY KEY NOT NULL,
                      USERNAME TEXT NOT NULL,
                      EMPNO TEXT NOT NULL,
                      MEMO1 TEXT NOT NULL,
                      MEMO2 TEXT NOT NULL,
                      MEMO3 TEXT NOT NULL,
                      MOMO4 TEXT NOT NULL);''')
    print("Table created successfully")
    conn.commit()
    conn.close()


def insert_table():
    conn, cursor = connect_db()

    plan_list = [{"username": "Ziyue Fu", "empno": "6063682"}]
    for plan in plan_list:
     cursor.execute("INSERT INTO JIRAUSER(ID, USERNAME, EMPNO, MEMO1, MEMO2, MEMO3, MOMO4) "
                   "VALUES({}, '{}', '{}', '{}', '{}', '{}', '{}')".format(randint(0, 9), plan["username"], plan["empno"], None, None, None, None))
    conn.commit()
    conn.close()


def query_table():
    conn, cursor = connect_db()
    cursor.execute("SELECT ID, USERNAME, EMPNO FROM JIRAUSER")
    users = []
    for row in cursor:
        user = {}
        user.update({"username": row[1], "empno": row[2]})
        users.append(user)
    print (users)
    conn.close()
    return users


def delete_table():
    conn, cursor = connect_db()
    conn.execute("DELETE FROM PLAN")
    conn.commit()
    conn.close()
    print("Table deleted successfully");


def get_users():
    users_json = json.loads(open(template_path + "/../static/users.json").read(), object_pairs_hook=OrderedDict)
    users = []
    for user in users_json:
        u = {}
        u.update({"username": users_json[user]["username"], "empno":user})
        users.append(u)
    return users


if __name__ == "__main__":

    # create_table()
    # insert_table()
    # query_table()
    get_users()