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
good_location = []

#there are 40 pages on the website and the pagination index increments by 24 each time
for page in range(0, 41*24, 24):
    print("Scrapping: " + baseURLpt1 + str(page) + baseURLpt2)
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
            ppw = round((ppm * 12)/ 52)
            if ppw > 580:
                good_price.append(False)
            else:
                good_price.append(True)
            price_per_week.append(ppw)
            price_per_month.append(ppm)

        #finds out when the property was added or reduced
        added = property.find_all("div", {"class":"propertyCard-contacts"})
        for item in added:
            added_or_reduced.append(item.find('span', {'data-bind':"text: addedOrReduced, css: {'propertyCard-contactsAddedOrReduced--recent': isRecent}"}).text)


        # finds the link to the property
        links = property.find_all('div', {"class":"propertyCard-details"})
        for link in links:
            for link1 in link.find_all('a'):
                if link1.has_attr('href'):
                    link_to_property.append("https://www.rightmove.co.uk" + link1.attrs['href'])

        # finds the address of the property
        addresses = property.find_all("address",{"class":"propertyCard-address"})
        for item in addresses:
            property_address = item.find('span', {"data-bind":"text: displayAddress"}).text
            if "NW1" in property_address:
                good_location.append(True)
            else:
                good_location.append(False)
            address.append(property_address)

#creates a list of rows
lst = []
zipped = zip(price_per_month, price_per_week, address, added_or_reduced, link_to_property, good_price, good_location)
for i in zipped:
    lst.append(i)


#creates a pandas DataFrame and converts it to a csv file
df = pandas.DataFrame(lst)
df.columns = ["PPM", 'PPW', "Address", "Added/Reduced Date", "Link", "Good Price", "Good Location"]
is_good_price = df['Good Price'] == True #checks to see if the property meets the requirements
df1 = df[is_good_price]
is_good_location = df1['Good Location'] == True #checks to see if the property meets the requirements
dfFinal = df1[is_good_location]
dfFinal.to_csv("Places.csv")
print("Finished")
