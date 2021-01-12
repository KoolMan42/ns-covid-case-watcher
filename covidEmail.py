
import ssl
import smtplib
import os
from jinja2 import Template
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def formatEmail(numOfCases: str, ):
    """
    Formats HTML template with number of cases.
    
    Parameters: 

    numOfCases (String): A string with the number of cases of COVID-19.

    Returns:
    A HTML string that contains the complete formatted template. 

    """
    try:
        f = open(os.path.join(
            os.getcwd(), "templates/emailTemplate.html"), 'r',  encoding="utf-8")
        textFromFile = f.readlines()
        rawEmail = "".join(textFromFile)
        # print(rawEmail)
        f.close()

    except(FileNotFoundError):
        print("File not found")

    emailTemplate = Template(rawEmail)
    renderedTemplate = emailTemplate.render(numOfCases=numOfCases)
    return(renderedTemplate)


def sendMailToEveryone(listOfReceivers:list, formatedEmail:str):
    """
    Sends out all the emails specified in the database 

    Perameters:

    listOfReceivers (List): A list of emails pulled from the database

    formatedEmail (String): A string that 
    
    """
    password = os.environ.get("PASSWD")

    sender_email = os.environ.get("SENDER_EMAIL")

    message = MIMEMultipart()
    message["Subject"] = "New COVID-19 Cases Announced"
    message["From"] = sender_email
    message["To"] = sender_email

    # Turn these into plain/html MIMEText objects
    messageText = MIMEText(formatedEmail, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(messageText)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.ehlo()
        # server.starttls()

        server.sendmail(
            sender_email, [sender_email] + listOfReceivers, message.as_string()
        )
