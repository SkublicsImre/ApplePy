import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime

t = 30

M = 0.0105


URL = 'https://www.portfolio.hu/arfolyam/EURHUF=X/euro'
headers = {"User-Agent": 'MyUserAgent'}

def check_page():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")

    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    price = soup.find(id="EURHUF").get_text()
    a = float(price)

    time.sleep(t)

    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    price = soup.find(id="EURHUF").get_text()
    b = float(price)

    if b == a:
        print("Current Time =", current_time)
        print ("Az elmúlt " + str(t/60) + " percben nem volt változás")
        print ("jelenlegi árfolyam: " + str(b) + "ft")        
        print ("")
    if b < a:
        print("Current Time =", current_time)
        print ("Az elmúlt " + str(t/60) + " percben a forint" + str(b-a) + "ponttal romlott az EU-hoz képest") 
        print ("jelenlegi árfolyam: " + str(b) + "Ft")
        print ("")
    if b > a:
        print("Current Time =", current_time)
        print ("Az elmúlt " + str(t/60) + " percben a forint" + str(a-b) + "ponttal javult az EU-hoz képest") 
        print ("jelenlegi árfolyam: " + str(b) + "Ft")
        print ("")
    if b - a > M:
        send_alert("BIG JUMP!")
    if a - b > M:
        send_alert("BIG FALL!")

def send_alert(a="none"):
    print (a)
    print ("")
    #server = smtplib.SMTP('smtp.gmail.com', 587)
    #server.ehlo()
    #server.starttls()
    #server.ehlo()

    #server.login('email adress', '************')
    #subject = 'spam'
    #msg = f"Subject: {subject}\n\n{a}"

    #server.sendmail(
     #  'email adress',
      # 'email adress',
       # msg
    #)
    #server.quit()

while (True):
    check_page()