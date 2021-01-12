import csv
from requests import get
from io import StringIO
from collections import deque
import datetime
import sched
import time
from covidEmail import sendMailToEveryone, formatEmail
from DB import getAllEmails, hasBeenSentToday, notSentToday

s = sched.scheduler(time.time, time.sleep)

LONG_SLEEP = 3600
SHORT_SLEEP = 60 * 3
HAS_EMAIL_BEEN_SENT_TODAY = False


def getCovidData():
    """
    Gets case data from the NS site
    """
    url = "https://novascotia.ca/coronavirus/data/ns-covid19-data.csv"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36"
    }
    try:
        response = get(url=url, headers=headers, verify=False)

    except:
        pass



    file = str(response.text).replace("\ufeff", "")

    spamreader = csv.reader(StringIO(file))

    x = deque(spamreader, 1)
    return(x[0])


def eventLoop():
    """
    The main event loop that re-queue's itself

    """
    global HAS_EMAIL_BEEN_SENT_TODAY

    # print(data)
    currentDate = datetime.datetime.now().strftime("%Y-%m-%d")
    data = getCovidData()
    if(currentDate != data[0]):
        notSentToday()
    if ((currentDate == data[0])):
        emails = getAllEmails()
        if(len(emails) != 0):
            formatedEmail = formatEmail(data[1])
            sendMailToEveryone(emails, formatedEmail)
            hasBeenSentToday(emails)

    s.enter(LONG_SLEEP, 1, eventLoop, )
    s.run()


def main():
    """
    Main function of the program

    """
    # s.enter(TIME_TO_SLEEP, 1, eventLoop, )
    eventLoop()
    # s.run()


if __name__ == '__main__':
    main()
