from selenium import webdriver
import requests
from bs4 import BeautifulSoup
from selenium import webdrive
import time

##given a web page url, return a list of links to all the {ad_class_name} on that web page.
#example usage:
    # ad_url ="https://www.behance.net/gallery/127057601/Blog-illustrations-for-Twingate"
    # ad_class = "ImageElement-image-SRv"
    # ad_link_type = "a"
    # inner_type = "class"
    # print(all_links_of_images(ad_url,ad_link_type,inner_type, ad_class))
def all_links_of_divs(url, div_type, inner_type, ad_class_name):
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
    project_links = soup.find_all(div_type, {inner_type: ad_class_name})
    links_list = []
    # Loop through each project link and find the link to the project's image
    for link in project_links:
        project_url = link["href"]
        links_list.append(project_url)
        
    return links_list
