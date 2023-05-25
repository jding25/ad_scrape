from selenium import webdriver
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import csv
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By

# from selenium.webdriver.support.select import Select
import time



#given a web page url, return a list of links to all the {ad_class_name} on that web page.

#usage: return a list of links of all ads on advertising page

# Launch the Chrome browser
url = "https://www.behance.net/search?tracking_source=typeahead_search_direct&search=advertising++business+card"
# Launch the Chrome browser
options = webdriver.ChromeOptions()
options.add_argument('--blink-settings=imagesEnabled=false')
# or alternatively we can set direct preference:
options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
# options = Options()
options.add_argument('--headless=new')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
# options.add_argument('--blink-settings=imagesEnabled=false')
driver = webdriver.Chrome(options=options)

# Navigate to a web page
requests.get(url)
driver.get(url)


#Scroll to the bottom of the page to load all content
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height


# Get the HTML of the fully-loaded page
html = driver.page_source
soup = BeautifulSoup(html, "html.parser")

# Find all links to projects on the page
project_links = soup.find_all('a', {'class':  "ProjectCoverNeue-coverLink-U39 js-project-cover-image-link js-project-link e2e-ProjectCoverNeue-link"})
# print(project_links)

image_link_list = []
# Loop through each project link and find the link to the project's image
for link in project_links:
    project_url = link["href"]
    image_link_list.append(project_url)
print(image_link_list) 


driver.quit()


# ad_url ="https://www.behance.net/search/projects?field=advertising&"
# ad_class = "ProjectCoverNeue-coverLink-U39 js-project-cover-image-link js-project-link e2e-ProjectCoverNeue-link"
# ad_link_type = "a"
# inner_type = "class"
# all_links_of_images(ad_url,ad_link_type,inner_type, ad_class)