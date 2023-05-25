import os
import csv
import json
import re
import requests
from bs4 import BeautifulSoup
from selenium import webdriver


# TODO: Include homosalate percentage!!
# TODO: pull ingredients ONLY from ingredients area
# TODO: refactor for redability, Python naming conventions and comment conventions
# TODO: revise where webdriver is opened and closed by best coding practices
"""
# SETUP CHROME TO RUN IN HEADLESS MODE
# Configure Chrome options to run in headless mode
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# Create a Chrome WebDriver instance
driver = webdriver.Chrome(options=options)
"""

# Retrieves page source code for dynamic web pages
def get_page_source(url):
    # Load the webpage
    driver.get(url)

    # Access hidden URLs and elements
    # Example: Click on a "Show More" button and wait for the new content to load
    #show_more_button = driver.find_element_by_id('manual_load_button') # ERROR
    #show_more_button.click()

    """
    # Scroll to the bottom of the dynamic webpage
    # Get the initial height of the page
    prev_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # Scroll to the bottom of the page
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
        # Wait a short time for content to load
        driver.implicitly_wait(10) # seconds
        # Get the new height of the page
        new_height = driver.execute_script("return document.body.scrollHeight")
        print(prev_height)
        print(new_height)
        # Break the loop if the page height remains unchanged (reached the bottom)
        if prev_height == new_height:
            break
        # Update the previous height
        prev_height = new_height
    """

    # Retrieve the updated page source with the hidden content
    html_content = driver.page_source
    return html_content

# download the HTML document with an HTTP GET request
# !!! Depreciated with Selenium - for static use only.
#response = requests.get("https://well.ca/searchresult.html?keyword=sunscreen")

#response = requests.get("https://well.ca/products/shiseido-clear-sunscreen-stick-spf_276474.html")
#response = requests.get("https://jackheatonlive.com/")

# parse the HTML content of the page listing all products
#page_source = get_page_source("https://well.ca/searchresult.html?keyword=sunscreen")
#soup = BeautifulSoup(page_source, "html.parser")
#soup = BeautifulSoup(response.content, "html.parser") # !!! Depreciated with Selenium - for static use only.

urls = []
#JENKY CODE FOR FAST download SCRAPING
def jenky_scrape(web_url):
    response = requests.get(web_url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Scrape all individual sunscreen product webpage urls from main page.
    product_elements = soup.find_all(class_="grid__item col-md-3 col-sm-4 col-xs-6") #returns a list of elements

    for product_element in product_elements:
        url = product_element.find("a")["href"]
        urls.append(url)

#jenky_scrape("https://well.ca/searchresult.html?keyword=sunscreen")
#jenky_scrape("https://well.ca/index.php?main_page=advanced_search_result&keyword=sunscreen&page=0")
#jenky_scrape("https://well.ca/index.php?main_page=advanced_search_result&keyword=sunscreen&page=1")
#jenky_scrape("https://well.ca/index.php?main_page=advanced_search_result&keyword=sunscreen&page=2")

#print(len(urls))
#print(urls[-1])

# This function works for static pages ONLY
def download_html(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        file_path = os.path.join(folder_path, filename)
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(response.text)
        print(f"HTML from {url} saved as {filename}")
    else:
        print(f"Failed to download HTML from {url}. Status code: {response.status_code}")


"""
# Create a subfolder to save the files
folder_path = 'html_files'
os.makedirs(folder_path, exist_ok=True)

# Download HTML from each URL and save it into separate files
for index, url in enumerate(urls):
    filename = f"html_{index}.html"  # Filename for each URL
    download_html(url, filename)
"""

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
    "homosalate_percentage": "homosalate percentage",
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
# TODO: rewrite as "write_products_to_file()
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


def scrape_product_page(url="", file_path=""):
    #response = requests.get("https://well.ca/products/shiseido-clear-sunscreen-stick-spf_276474.html")
    if url != "":
        response = requests.get(url)
        # parse the HTML content of the page listing specific product
        soup = BeautifulSoup(response.content, "html.parser")
    elif file_path != "":
        with open(file_path, 'r', encoding='utf-8') as file:
            html_content = file.read() # html content
        soup = BeautifulSoup(html_content, "html.parser")
    else:
        print("No page found.")
        return

    # Get the first reference of the word "homosalate" on the page
    #TODO: case handling of ingreidents like Homosalate.
    #homosalate = soup.findAll(string=re.compile('^Homosalate$'))
    homosalate = soup(string=re.compile('homosalate', re.IGNORECASE))
    propanediol = soup(string=re.compile('propanediol', re.IGNORECASE))
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
    homosalate_percentage = 0

    #Do I need to declare the variables up above to reference them in the "is None" case?
    # Check to see if key term returns an empty list. aka no references found.
    # TODO: add non-capitalized case
    if homosalate:
        print("yes true")
        # Find all the paragraphs containing the word "homosalate"
        homosalate_flag = True
        paragraphs = soup.find_all(string=re.compile(r'homosalate', re.IGNORECASE))
        # Loop through the paragraphs and extract the next word ending with "%"
        for paragraph in paragraphs:
            soupstring = str(paragraph)
            # Use regex to find the next word ending with "%"
            #match = re.search(r'(?<=Homosalate )\w+%', soupstring)
            match = re.search(r'Homosalate \d+.\d+', soupstring)
            if match:
                next_word = match.group(0)
                numbers_and_periods = re.findall(r'\d+\.?\d*', next_word)
                homosalate_percentage = float(numbers_and_periods[0])
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
        "homosalate_percentage": homosalate_percentage,
        "propanediol": propanediol_flag,
        "pg": pg_flag,
        "mineral": mineral_flag,
        "titanium": titanium_flag,
        "zinc": zinc_flag
    }

    # add the new product dictionary to the list
    sunscreen_products.append(new_sunscreen_product)
    writeToFile() # writes all to file every pass. Consider refactoring.


#scrape_product_page("https://well.ca/products/shiseido-clear-sunscreen-stick-spf_276474.html")

# SCRAPE DATA FROM ALL SUNSCREEN PAGES
# Iterates over only the first 20 elements.
"""
for url in urls[:20]:
    scrape_product_page(url)
    print("scraped")
    """

# TEST DATA SCRAP FROM OFFLINE
html_file_path = os.path.join('html_files', "html_0.html")
scrape_product_page(file_path=html_file_path)
html_file_path = os.path.join('html_files', "html_2.html")
scrape_product_page(file_path=html_file_path)

# SCRAPE DATA FROM ALL OFFLINE SUNSCREEN PAGES
# Continues until no more files found.
folder_path = 'html_files'
try:
    # Iterate through all files in the folder
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            scrape_product_page(file_path=file_path)
except FileNotFoundError:
    print("No files found in this folder.")



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

# Quit the WebDriver
#driver.quit()









