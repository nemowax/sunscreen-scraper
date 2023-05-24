import csv
import re
import requests
from bs4 import BeautifulSoup

# TODO: Include homosalate percentage
# TODO: pull ingredients ONLY from ingredients area

# download the HTML document with an HTTP GET request
response = requests.get("https://well.ca/searchresult.html?keyword=sunscreen")
#response = requests.get("https://well.ca/products/shiseido-clear-sunscreen-stick-spf_276474.html")
#response = requests.get("https://jackheatonlive.com/")

# parse the HTML content of the page listing all products
soup = BeautifulSoup(response.content, "html.parser")

# Scrape all individual sunscreen product webpage urls from main page.
product_elements = soup.find_all(class_="grid__item col-md-3 col-sm-4 col-xs-6") #returns a list of elements
urls = []
for product_element in product_elements:
    url = product_element.find("a")["href"]
    urls.append(url)

# SETUP THE PRODUCTS DICTIONARY
# Write products to a dictionary list
sunscreen_products = []

# Set up dictionary list columns for readable csv export
category_headings = {
    "title": "Title",
    "brand": "brand",
    "price": "price",
    "url": "url",
    "homosalate": "homosalate",
    "propanediol": "propanediol",
    "pg": "propylene glycol",
    "mineral": "mineral",
    "titanium": "titanium",
    "zinc": "zinc"
}
sunscreen_products.append(category_headings)

# TODO: make scraping logic a function and plug into error handling below
#error handling
# if the response is 2xx
#if response.ok:
    # scraping logic here...
#else:
    # log the error response
    # in case of 4xx or 5xx
#    print(response)



# EXPORT TO FILE AS CSV
def writeToFile():
    # create the "products.csv" file
    csv_file = open('products.csv', 'w', encoding='utf-8', newline='')

    # initialize a writer object for CSV data
    writer = csv.writer(csv_file)

    # convert each element of sunscreen_products
    # to CSV and add it to the output file
    for sunscreen_product in sunscreen_products:
        writer.writerow(sunscreen_product.values())

    # release the file resources
    csv_file.close()

def scrape_product_page(url):
    #response = requests.get("https://well.ca/products/shiseido-clear-sunscreen-stick-spf_276474.html")
    response = requests.get(url)
    # parse the HTML content of the page listing specific product
    soup = BeautifulSoup(response.content, "html.parser")

    # Get the first reference of the word "homosalate" on the page
    #TODO: case handling of ingreidents like Homosalate.
    #homosalate = soup.findAll(string=re.compile('^Homosalate$'))
    homosalate = soup(string=re.compile('homosalate', re.IGNORECASE))
    propanediol = soup(string=re.compile('propanedio', re.IGNORECASE))
    pg = soup(string=re.compile('propylene glycol', re.IGNORECASE))
    mineral = soup(string=re.compile('mineral', re.IGNORECASE))
    titanium = soup(string=re.compile('titanium', re.IGNORECASE))
    zinc = soup(string=re.compile('zinc', re.IGNORECASE))

    homosalate_flag = False
    propanediol_flag = False
    pg_flag = False
    mineral_flag = False
    titanium_flag = False
    zinc_flag = False

    #Do I need to declare the variables up above to reference them in the "is None" case?
    # Check to see if key term returns an empty list. aka no references found.
    # Check to see if key term returns an empty list. aka no references found.
    if homosalate:
        print("yes true")
        homosalate_flag = True
    if propanediol:
        propanediol_flag = True
    if pg:
        pg_flag = True
    if mineral:
        mineral_flag = True
    if titanium:
        titanium_flag = True
    if zinc:
        zinc_flag = True

    #if titanium is not None:
    #    titanium_flag = True

    # TODO: grab product name
    # TODO: grab product brand
    # TODO: formating to plain text
    title = soup.find("meta", property = "og:title") # product title
    brand = soup.find("meta", property = "og:brand")
    price = soup.find("meta", property = "og:price:amount")

    # Check this
    #volume = soup.find("h5", class = "product-info__subtitle")

    # TODO: Add for loop for multipLe sunscreen products from different pages
    # define a dictionary with the scraped data
    new_sunscreen_product = {
        "title": title["content"],
        "brand": brand["content"],
        "price": price["content"],
        "url": url,
        "homosalate": homosalate_flag,
        "propanediol": propanediol_flag,
        "pg": pg_flag,
        "mineral": mineral_flag,
        "titanium": titanium_flag,
        "zinc": zinc_flag
    }

    # add the new product dictionary to the list
    sunscreen_products.append(new_sunscreen_product)
    writeToFile() # writes all to file every pass. Consider refactoring.



# SCRAPE DATA FROM ALL SUNSCREEN PAGES
# Iterates over only the first 20 elements.
for url in urls[:20]:
    scrape_product_page(url)
    print("scraped")


#ERROR HANDLING
#print(brand["content"] if brand else "No meta brand given")
#print(title["content"] if title else "No meta title given")
#print(price["content"] if price else "No meta price given")

# TODO: grab product webpage
# TODO: grab product volume (mL)

#                                             <h5 class="product-info__subtitle">
#                             <span></span>
#                             <span>88 mL</span>
#                         </h5>


# TODO: Fix zinc flag in "Trending Items" section. From: "The Ordinary Niacinamide 10% + Zinc 1%"


# Error handling: making sure ingredient is present on the page
# before trying to access its data
#if homosalate is not None:
#    placeholder_string = homosalate["placeholder"]

# Extract only the page text, for parsing ease
#pageText = soup.getText()
#print(pageText)



# if the response is 2xx
"""

if response.ok:
    # scraping logic here...
    print(response.text)
else:
    # log the error response
    # in case of 4xx or 5xx
    print(response)

"""
#print the HTML code
#print(response.text)









