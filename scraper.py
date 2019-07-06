import requests
from bs4 import BeautifulSoup
import pandas

#used to impersonate a webpage else some sites wont provide access
headers = {'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'}

#get HTML content of the page and store it in soup
r=requests.get("https://www.rightmove.co.uk/property-to-rent/find.html?locationIdentifier=REGION%5E93941&maxBedrooms=3&minBedrooms=3&index=0&propertyTypes=flat&primaryDisplayPropertyType=flats&mustHave=&dontShow=&furnishTypes=&keywords=", headers=headers)
c = r.content
soup=BeautifulSoup(c, "html.parser")
#print(soup.prettify)

#find and extract the data regarding when the property was added or reduced
addedOrReduced = []
added = soup.find_all("div", {"class":"propertyCard-contacts"})
for item in added:
    #print(item.find('span', {'data-bind':"text: addedOrReduced, css: {'propertyCard-contactsAddedOrReduced--recent': isRecent}"}).text)
    addedOrReduced.append(item.find('span', {'data-bind':"text: addedOrReduced, css: {'propertyCard-contactsAddedOrReduced--recent': isRecent}"}).text)

#find and extract the data regarding the price per month and price per week for the property
all = soup.find_all("div", {"class":"propertyCard-rentalPrice-primary"})
ppm = []
ppw = []
for item in all:
    #print(item.find('span', {"class":"propertyCard-priceValue"}).text)
    price_month = item.find('span', {"class":"propertyCard-priceValue"}).text
    ppm.append(price_month)

#find and extract data regardng addresses of properties
addresses = []
addresses_content = soup.find_all("address",{"class":"propertyCard-address"})
for item in addresses_content:
    #print(item.find('span', {"data-bind":"text: displayAddress"}).text)
    addresses.append(item.find('span', {"data-bind":"text: displayAddress"}).text)
