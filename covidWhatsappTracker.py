import requests
import sys
from bs4 import BeautifulSoup
from twilio.rest import Client
import re
URL1="https://www.mohfw.gov.in/"


def check(string, sub_str):
    if (string.find(sub_str) == -1):
        return "NO"
    else:
        return "YES"



# client credentials are read from TWILIO_ACCOUNT_SID and AUTH_TOKEN
def notify_client_bymsg(totDeath,state,to_whatsapp_number):
    account_sid = 'ACba7b0a71237527388b15c0beXXXXXXXX'
    auth_token = 'f18f0c201994772b84bcXXXXXXX'
    client = Client(account_sid, auth_token)

    # this is the Twilio sandbox testing number
    from_whatsapp_number='whatsapp:+14155238886'
    # replace this number with your own WhatsApp Messaging number
    #to_whatsapp_number='whatsapp:+91XXXXX'

    client.messages.create(body="Total Number of Deaths in %s is %s"%(state,totDeath),
                       from_=from_whatsapp_number,
                       to=to_whatsapp_number)


page = requests.get(URL1)
soup = BeautifulSoup(page.content, 'html.parser')
flag=0
f = open("covid.txt", "w")
f.write(str(soup))
f.close()

f1=open("covid.txt","r")
Lines = f1.readlines()
stateName=sys.argv[1]
pattern="<td>"+stateName+"</td>"

count = 0
# Strips the newline character
for line in Lines:
    result = check(line, pattern)
    if result == 'YES':
        print("-----------******************-------------")
        flag=1

    if (flag==1) & (count < 4):
        count=count+1
        if(count ==1):
            line=line.replace("<td>","")
            line=line.replace("</td>","")
            print("State:",line)
        if(count==2):
            line=line.replace("<td>","")
            line=line.replace("</td>","")
            print("Active:",line)
        if(count==3):
            line=line.replace("<td>","")
            line=line.replace("</td>","")
            print("Total Recovered:",line)
        if(count==4):
            match=re.search(r'\d+',line)
            print(line)
            print("Match is",match.group())
            totalDeaths=int(match.group())
            print("Total Deaths:",totalDeaths)
            if(totalDeaths > 0):
                print("Notifying Client......")
                notify_client_bymsg(totalDeaths,stateName,'whatsapp:+9177XXXXX')


f1.close()

#print(soup)

