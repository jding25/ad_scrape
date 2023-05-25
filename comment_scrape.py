from selenium import webdriver
from bs4 import BeautifulSoup
import time
import re 
import pandas as pd
import numpy as np
from scrollProjectPage import *
from readFile import *

# return a datafrae of comments under a project given the projectURL
def get_comment_contents(projectURL):
    options = webdriver.ChromeOptions()
    options.add_argument('--blink-settings=imagesEnabled=false')
    options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})    
    options.add_argument('--headless=new')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=options)

    # # Navigate to a web page
    requests.get(projectURL)
    driver.get(projectURL)

    # Scroll to the bottom of the page to load all content
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        try:
            button = driver.find_element("xpath", "/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[2]/div[2]/div[4]/div[1]/div[1]/div[1]/div[1]/div[3]/span[1]")
            driver.execute_script("arguments[0].click();", button)
        except:
            pass
        try:
            see_more_comments = driver.find_element('xpath','/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[2]/div[2]/div[4]/div[1]/div[1]/div[1]/div[2]')
            driver.execute_script("arguments[0].click();", see_more_comments)
        except:
            pass
        if new_height == last_height:
            break
        last_height = new_height
            
    # Get the HTML of the fully-loaded page
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    work_id = re.findall("\d+",projectURL)[0]

    # find all the comments on the page
    comments_user_id_lst = []
    comments_time_lst = []
    comments_content_lst = []
    try:
        users = soup.find_all('a',{'class':'ProjectComment-userName-WSf'})
        for user in users:
            comments_user_id_lst.append(user['href'])
    except:
        pass

    try:
        comments_content = soup.find_all('div',{'class':'ProjectComment-comment-nUH'})
        for c in comments_content:
            comments_content_lst.append(c.text)
    except:
        pass

    try:
        times = soup.find_all('span',{'class':'ProjectComment-commentTimestamp-giY'})
        for t in times:
            comments_time_lst.append(t.text)
    except:
        pass
        
    driver.quit()
    work_id_lst = np.array([work_id] * len(comments_user_id_lst))
    time_stamp = np.array([time.time()] * len(comments_user_id_lst))
    
    df = pd.DataFrame({'user_id':comments_user_id_lst,
                       'work_id': work_id_lst,
                        'time':comments_time_lst,
                         'contents': comments_content_lst,
                          'time_stamp':time_stamp })
    return df
        

