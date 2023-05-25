from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time
import requests
from bs4 import BeautifulSoup
import locale
from readFile import *
import pandas as pd
import numpy as np


#given a web page url, return a list of links to all the {ad_class_name} on that web page.

#usage: return a list of links of all ads on advertising page

def all_links_of_appreciations(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    #num_appreciation = int(soup.findAll('td',{'class':'UserInfo-statColumn-NsR UserInfo-statValue-d3q'})[1].text)


    # Launch the Chrome browser
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--headless=new')
    options.add_argument('--blink-settings=imagesEnabled=false')
    options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})

    options.add_argument('--disable-gpu')

    driver = webdriver.Chrome(options=options)
    # driver = webdriver.Chrome()

    # Navigate to a web page
    requests.get(url)
    driver.get(url)
    time.sleep(6)
    works = driver.find_elements(By.CSS_SELECTOR,'a.AppreciationCover-coverLink-x1o js-project-cover-image-link')
    num_works= len(works)
    print(num_works)


    
    # # Scroll to the bottom of the page to load all content
    # last_height = driver.execute_script("return document.body.scrollHeight")
    # while True:
    #     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    #     time.sleep(2)
    #     new_height = driver.execute_script("return document.body.scrollHeight")
    #     if new_height == last_height:
    #         break
    #     last_height = new_height


    # # Get the HTML of the fully-loaded page
    # html = driver.page_source
    # driver.close()
    # driver.quit()
    # soup = BeautifulSoup(html, "html.parser")

    # # Find all links to projects on the page
    # project_links = soup.find_all(div_type, {inner_type: ad_class_name})
    # # print(project_links)

    # image_link_list = []
    # # Loop through each project link and find the link to the project's image
    # for link in project_links:
    #     project_url = link["href"]
    #     image_link_list.append(project_url)
        
    
    # return image_link_list


ad_url ="https://www.behance.net/Vertexer/appreciated"
print(all_links_of_appreciations(ad_url))