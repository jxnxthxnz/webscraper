from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import pandas as pd
import csv

options = webdriver.ChromeOptions()
options.add_argument("--incognito") #custom options, doesnt even work 
options.add_argument("--headless")
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_experimental_option("useAutomationExtension", False)
options.add_experimental_option("excludeSwitches",["enable-automation"])

driver = webdriver.Chrome("/usr/local/bin/chromedriver") #driver
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})") #tring to remove - chrome is being controlled by software
driver.get("https://www.google.com/") #main google url 
element = driver.find_element_by_name("q") #searchbar
element.clear()
keyWord = input("Enter Company: ") #enter your company
element.send_keys("Zoominfo" + " " + keyWord) #input phrase into google searchbar
element.send_keys(Keys.RETURN)

time.sleep(.5)
loadPage = driver.find_element_by_partial_link_text(keyWord) #first link has to have keyWord so just search for first element/link with keyWord
loadPage.click() #click first link
time.sleep(.5)

site = driver.page_source #driver has updated url, so use the newest url for beautifulsoup
soup = BeautifulSoup(site, "html.parser")

info = soup.find(class_="vertical-icons") #find outer class
newList = info.find_all(class_="vertical-gap") #list with all company info

fileData = open("txt.txt", "w") #text file with all the data

hqFind = newList[0] #find headquarter location
hq = hqFind.find(class_ = "content") #takes off hq, and only spits out acutal address
fileData.write("Headquarters:- " + hq.text.strip())
fileData.write("\n")
#print("Headquarters: " + hq.text.strip())
#print()

webFind = newList[2] #website
web = webFind.find(class_ = "content")
fileData.write("Website:- " + web.text.strip())
fileData.write("\n")
#print("Website: " + web.text.strip())
#print()

revFind = newList[3] #find revenue
rev = revFind.find(class_ = "content")
fileData.write("Revenue:- " + rev.text.strip())
fileData.write("\n")
#print("Revenue: " + rev.text.strip())
#print()

names = soup.find(class_ = "company-names") #alternate company names
name = names.find_all(class_ = "company-name")
#print("Alternate Company Names:", end = " ")
fileData.write("Alternate Company Names:- ")
for x in name:
    #print(x.text.strip(), end = ", ")
    fileData.write(x.text.strip() + "- ")
fileData.write("\n")
#print()
#print()

comp = soup.find(class_ = "competitors-content-wrapper") #competitors
compList = comp.find_all(class_ = "company-name link")
#print("Competitors: ", end = " ")
fileData.write("Competitors:- ")
for x in compList:
    #print(x.text.strip(), end = ", ")
    fileData.write(x.text.strip() + "- ")
fileData.write("\n")
#print()
#print()

ppl = soup.find_all(class_ = "org-chart") # top ppl at company
#print("Important MPPl:", end = " ")
fileData.write("Top Employees:- ")
for x in ppl:
    person = x.find(class_ = "person-name")
    #print(person.text.strip(), end = ", ")
    fileData.write(person.text.strip() + "- ")
fileData.write("\n")
#print()
#print()

tech = soup.find(class_ = "technologies-container") # tech stack 
eachTech = tech.find_all(class_ = "card-wrapper")
#print("Techstack: ", end = " ")
fileData.write("Techstack:- ")
for x in eachTech:
    techName = x.find(class_ = "limited")
    #print(techName.text.strip(), end = ", ")
    fileData.write(techName.text.strip() + "- ")
fileData.write("\n")

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
    elif index == 4:#only on line 6
        lines[index] = word[0:(len(word) - 5)]#remove last three things
    else:
        lines[index] = word[0:(len(word) - 3)]#remove last -
    index += 1
cleanText.close()

text = lines[0]
zero = text.split("-")
text = lines[1]
one = text.split("-")
text = lines[2]
two = text.split("-")
text = lines[3]
three = text.split("-")
text = lines[4]
four = text.split("-")
text = lines[5]
five = text.split("-")
text = lines[6]
six = text.split("-")
mega = [zero, one, two, three, four, five, six]
for x in mega:
    print(x)
csvFile = "csv.csv"

with open(csvFile, "w") as csvfile: 
    csvWriter = csv.writer(csvfile)
    csvWriter.writerows(mega)
