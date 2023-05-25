from selenium import webdriver
import requests
import time
from selenium.webdriver.common.by import By


# given a url to a project, get its likes, headline, catgory, time, views, and comment user url
def scrollPage(projectURL):
    options = webdriver.ChromeOptions()
    options.add_argument('--blink-settings=imagesEnabled=false')
    options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})    
    options.add_argument('--headless=new')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=options)

    # Navigate to a web page
    requests.get(projectURL)
    driver.get(projectURL)

    # Scroll to the bottom of the page to load all content
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        #find see more comments button
        try:
            button = driver.find_element("xpath", "/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[2]/div[2]/div[4]/div[1]/div[1]/div[1]/div[1]/div[3]/span[1]")
            driver.execute_script("arguments[0].click();", button)
        except:
            pass
        try:
            read_more = driver.find_element(By.XPATH,"//a[text()='Read More']")
            read_more.click()
            time.sleep(2)
        except:
            pass
        if new_height == last_height:
            break
        last_height = new_height

    # Get the HTML of the fully-loaded page
    html = driver.page_source
    driver.quit()
    return html