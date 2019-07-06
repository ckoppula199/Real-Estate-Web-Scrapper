import requests
from bs4 import BeautifulSoup
import pandas
from re import sub
from decimal import Decimal

#allows program to mimic a webpage as some sites don't allow access otherwise
headers = {'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'}
r=requests.get("https://www.rightmove.co.uk/property-to-rent/find.html?locationIdentifier=REGION%5E93941&maxBedrooms=3&minBedrooms=3&index=0&propertyTypes=flat&primaryDisplayPropertyType=flats&mustHave=&dontShow=&furnishTypes=&keywords=", headers=headers)
c = r.content

#two parts of the url used to navigate through pagination by changing the index in the middle
baseURLpt1 = "https://www.rightmove.co.uk/property-to-rent/find.html?locationIdentifier=REGION%5E93941&maxBedrooms=3&minBedrooms=3&index="
baseURLpt2 = "&propertyTypes=flat&primaryDisplayPropertyType=flats&mustHave=&dontShow=&furnishTypes=&keywords="

#store html content of webpage in soup variable
soup=BeautifulSoup(c, "html.parser")

#arrays to store data of properties
added_or_reduced = []
link_to_property = []
price_per_month = []
price_per_week = []
address = []
good_price = []

#there are 40 pages on the website and the pagination index increments by 24 each time
for page in range(0, 41*24, 24):
    print("Finished inspecting: " + baseURLpt1 + str(page) + baseURLpt2)
    r=requests.get(baseURLpt1 + str(page) + baseURLpt2, headers = headers)
    c = r.content
    soup = BeautifulSoup(c, "html.parser")

    #gets content of every property from that page
    every_property = soup.find_all('div', {'class':"l-searchResult is-list is-not-grid"})

    # loops through each property in the current selected page
    for property in every_property:

        #finds the price per week and price per month of each property, assign True is ppw is less than 580, false otherwise
        prices = property.find_all("div", {"class":"propertyCard-rentalPrice-primary"})
        for item in prices:
            money = item.find('span', {"class":"propertyCard-priceValue"}).text
            ppm = Decimal(sub(r'[^\d.]', '', money))
            ppw = round((value * 12)/ 52)
            if ppw > 580:
                good_price.append(False)
            else:
                good_price.append(True)
            price_per_week.append(ppw)
            price_per_month.append(ppm)

        #finds out when the property was added or reduced
        added = thing.find_all("div", {"class":"propertyCard-contacts"})
        for item in added:
            added_or_reduced.append(item.find('span', {'data-bind':"text: addedOrReduced, css: {'propertyCard-contactsAddedOrReduced--recent': isRecent}"}).text)


        links = thing.find_all('div', {"class":"propertyCard-details"})
        for link in links:
            for link1 in link.find_all('a'):
                if link1.has_attr('href'):
                    link_to_property.append("https://www.rightmove.co.uk" + link1.attrs['href'])
