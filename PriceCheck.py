# Amazon Price Checker
# Made by Seb Green
# See readme.md for guidance on how to use

import smtplib
import sys
import time
import argparse
from requests_html import HTMLSession

CRED = '\033[91m'
CREDBG = '\033[41m'
CYELLOW = '\033[33m'
CGREEN = '\033[32m'
CBLUEBG = '\033[44m'
CEND = '\033[0m'

wait_time = 60
gmail_user = ''
gmail_password = ''
sendto = ''

# Get number of items
def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

# Read items file and check price for each item
def readfile():
    f = open('items.txt', 'r')
    lines = f.readlines()

    session = HTMLSession()

    for line in lines:
        item_values = line.replace("['", '').replace("']", '').split("','")
        item_name = item_values[0]
        url = item_values[1]
        lowerbound = float(item_values[2])
        upperbound = float(item_values[3])

        amazonprice = checkprice(session, item_name, url)

        if amazonprice != -1:
            if amazonprice <= lowerbound:
                print(CBLUEBG + '{} has passed your lower boundary!'.format(item_name) + CEND + '\n' + CBLUEBG + '{} : {} (Lower bound : {})'.format(item_name,amazonprice,lowerbound) + CEND)
                sendemail(item_name, url, lowerbound, amazonprice, 0)
            elif amazonprice >= upperbound:
                print(CREDBG + '{} has passed your upper boundary!'.format(item_name) + CEND + '\n' + CREDBG + '{} : {} (Upper bound : {})'.format(item_name,amazonprice,upperbound) + CEND)
                sendemail(item_name, url, upperbound, amazonprice, 1)
            else:
                print(CGREEN + '{} : {}'.format(item_name, amazonprice) + CEND + ' (Lower bound : {}, Upper bound : {})'.format(lowerbound, upperbound))

        time.sleep(5)

    session.close()


def checkprice(session, item_name, url):
    if 'amazon.co.uk/' in url:

        response = session.get(url, verify=True)
        price = response.html.find('#priceblock_ourprice', first=True)

        if price is None:

            price = response.html.find('#priceblock_dealprice', first=True)

            if price is None:

                print(CRED + "Couldn't get price of {}. Product is probably not for sale via Amazon".format(item_name) + CEND)
                return -1

        if isnotprimeornostock(response):
            print(CREDBG + "{} is either not prime or out of stock! Sending an email...".format(item_name) + CEND)
            sendemail(item_name, url, 0, 0, 2)
            return -1

        price = price.text.split('£')[1]

        return float(price)

    else:
        print(CYELLOW + 'Not an Amazon URL' + CEND)
        return -1


def isnotprimeornostock(response):
    isprime = response.html.find('div.a-checkbox > label > span', first=True)
    if isprime is None:
        return True
    return False


def sendemail(item_name, url, boundary, amazonprice, mode):

    if mode == 0:
        sent_from = 'Amazon Price Tracker'
        subject = 'LOWER BOUND: {} price alert!'.format(item_name)
        body = '{} passed your lower boundary!\n\nAmazon Price: {}\nLower Boundary: {}\nURL: {}'.format(item_name, amazonprice, boundary, url)
    elif mode == 1:
        sent_from = 'Amazon Price Tracker'
        subject = 'UPPER BOUND: {} price alert!'.format(item_name)
        body = '{} passed your upper boundary!\n\nAmazon Price: {}\nUpper Boundary: {}\nURL: {}'.format(item_name, amazonprice, boundary, url)
    else:
        sent_from = 'Amazon Price Tracker'
        subject = '{} is either not prime or out of stock!'.format(item_name)
        body = '{} is either not prime or out of stock!\n\nURL: {}'.format(item_name, url)
    email_text = """From: %s\nTo: %s\nSubject: %s\n\n%s """ % (sent_from, ", ".join(sendto), subject, body)

    try:
        smtpserver = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtpserver.ehlo()
        smtpserver.login(gmail_user, gmail_password)
        smtpserver.sendmail(sent_from, sendto, email_text)
        smtpserver.close()

        if mode == 0:
            print(CBLUEBG + 'Email has been sent to {}'.format(sendto) + CEND)
        else:
            print(CREDBG + 'Email has been sent to {}'.format(sendto) + CEND)

    except:
        print(CREDBG + 'Email failed to send' + CEND)


parser = argparse.ArgumentParser()
parser.add_argument("--time", "-t", help="set wait time until next automatic price check", type=int)
parser.add_argument("--recipient", "-r", help="set email address to receive alerts")
parser.add_argument("--email", "-e", help="set gmail address to send alerts from", required=True)
parser.add_argument("--password", "-p", help="set password to the gmail account", required=True)

args = parser.parse_args()

if args.time:
    wait_time = args.time
if args.email:
    gmail_user = args.email
if args.password:
    gmail_password = args.password
if args.recipient:
    sendto = [args.recipient]
else:
    sendto = [gmail_user]

try:
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(gmail_user, gmail_password)
    server.close()

    print(CYELLOW + str(time.strftime("%H:%M:%S ")) + '-' * 50 + CEND)
    print(CGREEN + "Successfully connected to Gmail's SMTP server" + CEND)
except:
    sys.exit(CRED + 'Could not connect to gmail. Check account credentials' + CEND)

print(CGREEN + 'Time between price checks: {} minutes'.format(wait_time) + CEND)
print(CGREEN + 'No. of products to price check: {}'.format(file_len('items.txt')) + CEND)
print(CGREEN + 'Sending alerts to: {}'.format(sendto) + CEND)
while True:
    print(CYELLOW + str(time.strftime("%H:%M:%S ")) + '-' * 50 + CEND)
    readfile()
    time.sleep(wait_time * 60)
