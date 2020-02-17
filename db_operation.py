import sqlite3
import read_excel


def connect_db():
    conn = sqlite3.connect('test2')
    cursor = conn.cursor()
    print ("Opened database successfully")
    return conn, cursor


def create_table():
    conn, cursor = connect_db()
    cursor.execute('''CREATE TABLE PLAN (ID INT PRIMARY KEY NOT NULL,
                      TIME TEXT NOT NULL,
                      PERIOD TEXT NOT NULL,
                      ITEM TEXT NOT NULL,
                      ISFINISHED TEXT NOT NULL);''')
    print("Table created successfully")
    conn.commit()
    conn.close()


def insert_table():
    conn, cursor = connect_db()
    # cursor.execute("INSERT INTO PLAN(ID, TIME, PERIOD, ITEM, ISFINISHED) "
    #                "VALUES(1, 'morning', '10:00-11:00', 'List all the work', 'Yes')")
    plan_list = read_excel.read_excel()
    i=0
    for plan in plan_list:
     i+=1
     cursor.execute("INSERT INTO PLAN(ID, TIME, PERIOD, ITEM, ISFINISHED) "
                   "VALUES({}, '{}', '{}', '{}', '{}')".format(i, plan["time"], plan["period"], plan["item"], plan["isFinished"]))
    conn.commit()
    conn.close()


def query_table():
    conn, cursor = connect_db()
    cursor.execute("SELECT ID, TIME, PERIOD ,ITEM, ISFINISHED FROM PLAN")
    for row in cursor:
        print ("ID=", row[0])
        print ("TIME=", row[1])
        print ("PERIOD=", row[2])
        print ("ITEM=", row[3])
        print ("ISFINISHED=", row[4])
    conn.close()


def delete_table():
    conn, cursor = connect_db()
    conn.execute("DELETE FROM PLAN")
    conn.commit()
    conn.close()
    print("Table deleted successfully");


if __name__ == "__main__":
    #delete_table()
    #query_table()
    #create_table()
    #insert_table()
    query_table()