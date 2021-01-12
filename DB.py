import os
import psycopg2



def getDatabaseConnection():
    docker = "docker"
    con = psycopg2.connect(host="db" ,dbname=docker,user=docker,password=os.environ.get("DATABASE_CONNECTION_PASSWORD"))
    cur = con.cursor()
    return cur, con


def getAllEmails():
    """
    Gets all the emails from the database and returns them as a list
    """
    cur, con = getDatabaseConnection()

    cur.execute("select email from person where has_gotten_email_today = False")
    emails = []
    for i in cur.fetchall():
        emails.append(i[0])
    con.close()

    return emails




def hasBeenSentToday(listOfEmails):
    cur, con = getDatabaseConnection()

    for i in listOfEmails:
        sql = "UPDATE person SET has_gotten_email_today = True WHERE email = '{email}';".format(email=i)
        cur.execute(sql)
    cur.execute("commit;")
    con.close()


def notSentToday():
    cur, con = getDatabaseConnection()
    cur.execute("UPDATE person SET has_gotten_email_today = False; commit;")

    con.close()
