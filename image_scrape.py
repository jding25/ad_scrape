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
from csv import writer
import json
import requests
from PIL import Image
from io import BytesIO
import json


from selenium import webdriver
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time

def all_links_of_images(url):
    # Launch the Chrome browser
    options = webdriver.ChromeOptions()
    options.add_argument('--blink-settings=imagesEnabled=false')
    options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
    options.add_argument('--headless=new')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=options)

    # Navigate to a web page
    requests.get(url)
    driver.get(url)

    # Scroll to the bottom of the page to load all content
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
    driver.close()
    driver.quit()
    soup = BeautifulSoup(html, "html.parser")

    # Find all links to projects on the page
    project_links = soup.find_all("class", {"img": "ImageElement-image-SRv"})
    # print(project_links)

    image_link_list = []
    # Loop through each project link and find the link to the project's image
    for link in project_links:
        project_url = link["src"]
        image_link_list.append(project_url)

    return image_link_list

#("https://www.behance.net/search?tracking_source=typeahead_search_direct&search=advertising++poster/post+card", )
ad_url ="https://www.behance.net/gallery/127057601/Blog-illustrations-for-Twingate"
print(all_links_of_images(ad_url))