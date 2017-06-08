# ZachC16/@zcgolf16
# Simple STEEM price text alerts
# Version 1.2
# June 8, 2017

from email.mime.text import MIMEText
import smtplib
from urllib.request import *
import ast
import time

def alertRun():
    # Setup
    print("Starting up... NOTE: Start-up involves calling APIs, so be patient!")
    USD = USDToSTEEMAPICall()
    BTC = BTCToSTEEMAPICall()
    GBP = GBPToSTEEMAPICall()
    EUR = EURToSTEEMAPICall()
    clear()
    print("\n\n----------------Currency Pair List----------------\n\n1 - USD/STEEM ($"+str(USD)+")\n2 - BTC/STEEM ("+str(BTC)+" BTC)\n3 - GBP/STEEM (£"+str(GBP)+")\n4 - EUR/STEEM (€"+str(EUR)+")")
    alertCurrencyPair = int(input("Enter the number corresponding to the currency pair you wish to be alerted about:"))
    while alertCurrencyPair != 1 and alertCurrencyPair != 2 and alertCurrencyPair != 3 and alertCurrencyPair != 4:
        print("You entered an invalid number. Please try again.")
        alertCurrencyPair = int(input("Enter the number corresponding to the currency pair you wish to be alerted about:"))
    alert = float(input("What price of STEEM would you like to be alerted at (NOTE: Only enter a float number. Do not enter any symbols or letters: "))
    print("\n\n----------------Alert Setup----------------\n\n")
    smtpserver = str(input("What is your email service's SMTP server domain (i.e. smtp.gmail.com for gmail)?: "))
    smtplogin = str(input("What is your email address?: "))
    smtppassword = str(input("What is your email password? (NOTE: Your password will be echoed.): "))
    phonenumber = str(input("What is your phone number?: "))
    while len(phonenumber) != 10:
        print("The number entered is invalid. Please try again.")
        phonenumber = str(input("What is your phone number?: "))
    print("\n\n----------------Carrier List----------------\n\n1 - AT&T\n2 - Cricket\n3 - MetroPCS\n4 - Sprint\n5 - T-Mobile (U.S.)\n6 - Verzion Wireless\nAny Other Number - Other")
    txtgateway = (int(input("Enter the number corresponding to your cell carrier from the list above: ")))
    if txtgateway == 1:
        txtgateway = "@txt.att.net"
        print("AT&T selected.\n")
    elif txtgateway == 2:
        txtgateway = "@mms.cricketwireless.net"
        print("Cricket Wireless selected.\n")
    elif txtgateway == 3:
        txtgateway = "@mymetropcs.com"
        print("MetroPCS selected.\n")
    elif txtgateway == 4:
        txtgateway = "@messaging.sprintpcs.com"
        print("Sprint selected.\n")
    elif txtgateway == 5:
        txtgateway = "@tmomail.net"
        print("T-Mobile (U.S.) selected.\n")
    elif txtgateway == 6:
        txtgateway = "@vtext.com"
        print("Verzion selected.\n")
    else:
        txtgateway = str(input("What is your mobile carrier's sms gateway domain?: "))


    alertTrigger = True

    # USD/STEEM alerts
    if alertCurrencyPair == 1:
        priceAtTimeOfAlert = USDToSTEEMAPICall()
    elif alertCurrencyPair == 2:
        priceAtTimeOfAlert = BTCToSTEEMAPICall()
    elif alertCurrencyPair == 3:
        priceAtTimeOfAlert = GBPToSTEEMAPICall()
    elif alertCurrencyPair == 4:
        priceAtTimeOfAlert = EURToSTEEMAPICall()
    print(priceAtTimeOfAlert)
    if alert > priceAtTimeOfAlert:
        while alertTrigger == True:
            if alertCurrencyPair == 1:
                currentPrice = USDToSTEEMAPICall()
                currency = "$"
            elif alertCurrencyPair == 2:
                currentPrice = BTCToSTEEMAPICall()
                currency = " BTC"
            elif alertCurrencyPair == 3:
                currentPrice = GBPToSTEEMAPICall()
                currency = " GBP"
            elif alertCurrencyPair == 4:
                currentPrice = EURToSTEEMAPICall()
                currency = " EURO"
            time.sleep(2)

            if alert <= currentPrice:
                sendMessage(smtplogin, smtppassword, phonenumber, txtgateway, smtpserver, "hit/risen above", alert, currency)
                alertTrigger = False


    elif alert < priceAtTimeOfAlert:
        while alertTrigger == True:
            if alertCurrencyPair == 1:
                currentPrice = USDToSTEEMAPICall()
                currency = "$"
            elif alertCurrencyPair == 2:
                currentPrice = BTCToSTEEMAPICall()
                currency = " BTC"
            elif alertCurrencyPair == 3:
                currentPrice = GBPToSTEEMAPICall()
                currency = " GBP"
            elif alertCurrencyPair == 4:
                currentPrice = EURToSTEEMAPICall()
                currency = " EURO"
            time.sleep(2)

            if alert >= currentPrice:
                sendMessage(smtplogin, smtppassword, phonenumber, txtgateway, smtpserver, "hit/dropped below", alert, currency)
                alertTrigger = False

# BTC/STEEM price API call
def BTCToSTEEMAPICall():
    STEEMPrice = 0
    while STEEMPrice == 0:
        try:
            response = urlopen("https://min-api.cryptocompare.com/data/generateAvg?fsym=STEEM&tsym=BTC&markets=Poloniex,HitBTC")
            STEEMPrice = response.read()
            STEEMPrice = STEEMPrice.decode("utf-8")
            STEEMPrice = ast.literal_eval(STEEMPrice)
            STEEMPrice = float(STEEMPrice['RAW']['PRICE'])
        except:
            print("Connection error.")

    print(STEEMPrice)

    return STEEMPrice


# USD/STEEM price API call
def USDToSTEEMAPICall():
    BTCPriceUSD = 0
    STEEMPrice = BTCToSTEEMAPICall()
    while BTCPriceUSD == 0:
        try:
            response = urlopen("http://api.coindesk.com/v1/bpi/currentprice.json")
            BTCPrice = response.read()
            BTCPrice = BTCPrice.decode("utf-8")
            BTCPrice = ast.literal_eval(BTCPrice)
            BTCPriceUSD = BTCPrice['bpi']['USD']['rate'].replace(',','')
            BTCPriceUSD = float(BTCPriceUSD)
        except:
            print("Connection error.")

    STEEMPriceUSD = BTCPriceUSD*STEEMPrice
    print(STEEMPriceUSD)

    return STEEMPriceUSD


# GBP/STEEM price API call
def GBPToSTEEMAPICall():
    BTCPriceGBP = 0
    STEEMPrice = BTCToSTEEMAPICall()
    while BTCPriceGBP == 0:
        try:
            response = urlopen("http://api.coindesk.com/v1/bpi/currentprice.json")
            BTCPrice = response.read()
            BTCPrice = BTCPrice.decode("utf-8")
            BTCPrice = ast.literal_eval(BTCPrice)
            BTCPriceGBP = BTCPrice['bpi']['GBP']['rate'].replace(',','')
            BTCPriceGBP = float(BTCPriceGBP)
        except:
            print("Connection error.")

    STEEMPriceGBP = BTCPriceGBP*STEEMPrice
    print(STEEMPriceGBP)

    return STEEMPriceGBP


# EUR/STEEM price API call
def EURToSTEEMAPICall():
    BTCPriceEUR = 0
    STEEMPrice = BTCToSTEEMAPICall()
    while BTCPriceEUR == 0:
        try:
            response = urlopen("http://api.coindesk.com/v1/bpi/currentprice.json")
            BTCPrice = response.read()
            BTCPrice = BTCPrice.decode("utf-8")
            BTCPrice = ast.literal_eval(BTCPrice)
            BTCPriceEUR = BTCPrice['bpi']['EUR']['rate'].replace(',','')
            BTCPriceEUR = float(BTCPriceEUR)
        except:
            print("Connection error.")

    STEEMPriceEUR = BTCPriceEUR*STEEMPrice
    print(STEEMPriceEUR)

    return STEEMPriceEUR


def sendMessage(smtplogin, smtppassword, phonenumber, txtgateway, smtpserver, updown, alert, currency):
    msg = MIMEText("STEEM's price has "+str(updown)+" "+str(alert)+str(currency)+"!")
    print("STEEM's price has "+str(updown)+" "+str(alert)+str(currency)+"!")
    msg['Subject'] = "STEEM price alert from steem-alerts!"
    msg['From'] = smtplogin
    msg['To'] = phonenumber+txtgateway
    send = smtplib.SMTP_SSL(smtpserver)
    send.login(smtplogin, smtppassword)
    send.sendmail(msg['From'], [msg['To']], msg.as_string())
    print("Sent.")
    send.quit()


def clear():
    print("\n"*120)





alertRun()
