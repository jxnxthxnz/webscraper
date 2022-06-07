from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time

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

hqFind = newList[0] #find headquarter location
hq = hqFind.find(class_ = "content") #takes off hq, and only spits out acutal address
print("Headquarters: " + hq.text.strip())
print()

webFind = newList[2] #website
web = webFind.find(class_ = "content")
print("Website: " + web.text.strip())
print()

revFind = newList[3] #find revenue
rev = revFind.find(class_ = "content")
print("Revenue: " + rev.text.strip())
print()

names = soup.find(class_ = "company-names") #alternate company names
name = names.find_all(class_ = "company-name")
print("Alternate Company Names:", end = " ")
for x in name:
    print(x.text.strip(), end = ", ")
print()
print()

comp = soup.find(class_ = "competitors-content-wrapper") #competitors
compList = comp.find_all(class_ = "company-name link")
print("Competitors: ", end = " ")
for x in compList:
    print(x.text.strip(), end = ", ")
print()
print()

ppl = soup.find_all(class_ = "org-chart") # top ppl at company
print("Important Motherfuckers:", end = " ")
for x in ppl:
    person = x.find(class_ = "person-name")
    print(person.text.strip(), end = ", ")
print()
print()

tech = soup.find(class_ = "technologies-container") # tech stack 
eachTech = tech.find_all(class_ = "card-wrapper")
print("Techstack:", end = " ")
for x in eachTech:
    techName = x.find(class_ = "limited")
    print(techName.text.strip(), end = ", ")