from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
#from fake_useragent import UserAgent
import time
import pandas as pd
import csv

c = webdriver.ChromeOptions()
c.add_argument("--incognito") #incognito mode
#c.add_argument("--headless") #page doesn't show up
c.add_argument('--disable-blink-features=AutomationControlled')
c.add_experimental_option("useAutomationExtension", False)
c.add_experimental_option("excludeSwitches",["enable-automation"])
#ua = UserAgent()
#userAgent = ua.random
#print(userAgent)
#c.add_argument(f'user-agent={userAgent}')

driver = webdriver.Chrome("/usr/local/bin/chromedriver", options=c) #driver
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})") #tring to remove - chrome is being controlled by software
driver.implicitly_wait(0.5)
driver.get("https://www.google.com/") #main google url 
element = driver.find_element_by_name("q") #searchbar
element.clear()
keyWord = input("Enter Company (Make sure your capitalization and spelling are correct): ") #enter your company
element.send_keys("Zoominfo" + " " + keyWord) #input phrase into google searchbar
element.send_keys(Keys.RETURN)

loadPage = driver.find_element_by_partial_link_text(keyWord) #first link has to have keyWord so just search for first element/link with keyWord
loadPage.click() #click first link

site = driver.page_source #driver has updated url, so use the newest url for beautifulsoup
soup = BeautifulSoup(site, "html.parser")

info = soup.find(class_="vertical-icons") #find outer class
try: 
    newList = info.find_all(class_="vertical-gap") #list with all company info
except: 
    print("Error occured, please rerun the program. The issue either lies in the spelling of the company requested, or ZoomInfo has detected the use of automated tools. To solve the latter, close the program and Google Chrome and wait a bit before rerunning.")
    driver.close()
    quit()

fileData = open("txt.txt", "w") #text file with all the data

try:
    hqFind = newList[0] #find headquarter location
    hq = hqFind.find(class_ = "content") #takes off hq, and only spits out acutal address
    fileData.write("Headquarters:_ " + hq.text.strip())
    fileData.write("\n")
except:
    pass

try:
    webFind = newList[2] #website
    web = webFind.find(class_ = "content")
    fileData.write("Website:_ " + web.text.strip())
    fileData.write("\n")
except: 
    pass

try:
    revFind = newList[3] #find revenue
    rev = revFind.find(class_ = "content")
    fileData.write("Revenue:_ " + rev.text.strip())
    fileData.write("\n")
except:
    pass

try:
    names = soup.find(class_ = "company-names") #alternate company names
    name = names.find_all(class_ = "company-name")
    fileData.write("Alternate Company Names:_ ")
    for x in name:
        fileData.write(x.text.strip() + "_ ")
    fileData.write("\n")
except: 
    pass

try:
    comp = soup.find(class_ = "competitors-content-wrapper") #competitors
    compList = comp.find_all(class_ = "company-name link")
    fileData.write("Competitors:_ ")
    for x in compList:
        fileData.write(x.text.strip() + "_ ")
    fileData.write("\n")
except:
    pass

try:
    ppl = soup.find_all(class_ = "org-chart") # top ppl at company
    fileData.write("Top Employees:_ ")
    for x in ppl:
        person = x.find(class_ = "person-name")
        fileData.write(person.text.strip() + "_ ")
    fileData.write("\n")
except:
    pass

try:
    tech = soup.find(class_ = "technologies-container") # tech stack 
    eachTech = tech.find_all(class_ = "card-wrapper")
    fileData.write("Techstack:_ ")
    for x in eachTech:
        techName = x.find(class_ = "limited")
        fileData.write(techName.text.strip() + "_ ")
    fileData.write("\n")
except:
    pass

fileData.close()

cleanText = open("txt.txt", "r")#process my text
lines = []#store data for cleaning
for x in range(7): #attach lines in text file to array
    lines.append(cleanText.readline())

index = 0 #starting index of line to fix
for x in range(7):
    word = lines[index]
    if index < 3:
        lines[index] = word[0:(len(word) - 1)]
    else:
        lines[index] = word[0:(len(word) - 3)]#remove last -
    index += 1
cleanText.close()

text = lines[0]
zero = text.split("_")
text = lines[1]
one = text.split("_")
text = lines[2]
two = text.split("_")
text = lines[3]
three = text.split("_")
text = lines[4]
four = text.split("_")
text = lines[5]
five = text.split("_")
while (' ' in five):
    five.remove(' ')
text = lines[6]
six = text.split("_")
mega = [zero, one, two, three, four, five, six]
for x in mega:
    print(x)
csvFile = "csv.csv"

with open(csvFile, "w") as csvfile: 
    csvWriter = csv.writer(csvfile)
    csvWriter.writerows(mega)

driver.close()