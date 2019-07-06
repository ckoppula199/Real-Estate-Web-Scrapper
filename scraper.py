import requests
from bs4 import BeautifulSoup
import pandas
from re import sub
from decimal import Decimal

headers = {'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'}
r=requests.get("https://www.rightmove.co.uk/property-to-rent/find.html?locationIdentifier=REGION%5E93941&maxBedrooms=3&minBedrooms=3&index=0&propertyTypes=flat&primaryDisplayPropertyType=flats&mustHave=&dontShow=&furnishTypes=&keywords=", headers=headers)
c = r.content
baseURLpt1 = "https://www.rightmove.co.uk/property-to-rent/find.html?locationIdentifier=REGION%5E93941&maxBedrooms=3&minBedrooms=3&index="
baseURLpt2 = "&propertyTypes=flat&primaryDisplayPropertyType=flats&mustHave=&dontShow=&furnishTypes=&keywords="

soup=BeautifulSoup(c, "html.parser")
#print(soup.prettify)

added_or_reduced = []
link_to_property = []
b = []
f = []
cc = []
good_price = []
