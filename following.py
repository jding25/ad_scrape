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

# example: following_scrape('selahattiniltas')
def following_scrape(user_url):
    URL = "https://www.behance.net/"+user_url

    #get number of followings
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    stats = soup.findAll('tr',{'class':'UserInfo-statRow-wH9'})
    if stats:
        if stats[-1].find('td').text == 'Following':
            locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
            num_following = stats[-1].find('a').text
            if ',' in num_following:
                num_following = num_following.replace(',','')
            num_following = int(num_following)
            print(num_following)
        else:
            return ['']
    else:
        return ['']


    # launch the browser and go to the URL
    options = webdriver.ChromeOptions()
    options.add_argument('--blink-settings=imagesEnabled=false')
    # or alternatively we can set direct preference:
    options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
    options.add_argument('--headless=new')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=options)
    driver.get(URL)
    time.sleep(2)

    #locate the follower link: change this to following
    following_button = driver.find_element(By.CSS_SELECTOR,"a[class='UserInfo-statValue-d3q']")
    driver.execute_script("arguments[0].click();", following_button)
    time.sleep(2)
    users = driver.find_elements(By.CSS_SELECTOR,'li.Following-profileRowItem-thx')
    num_user = len(users)
    if num_user == 0:
        return ['']
    while True:
        try:
            driver.execute_script("arguments[0].scrollIntoView();", users[num_user-1] )
            time.sleep(2)
            new_users = driver.find_elements(By.CSS_SELECTOR,'li.Following-profileRowItem-thx')
            new_num_users = len(new_users)
            if new_num_users == num_user:
                break
            users = new_users
            num_user = new_num_users
        except:
            time.sleep(2)
            users = driver.find_elements(By.CSS_SELECTOR,'li.Following-profileRowItem-thx')
            num_user = len(users)

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    driver.close()
    driver.quit()

    followings = soup.find_all('a',{'class':'ProfileRow-profileLink-hvq e2e-ProfileRow-link'})
    following_list = []
    for f in followings:
        following_list.append(f['href'].split('/')[-1])
    return following_list


# example user_list = read_list('card_user_list'), index = 0
def generate_following_table(user_list, index):
    # if there is already a table, comment 2 lines below
    # tbl = pd.DataFrame(columns = ['user_id', 'following_id'])
    # tbl.to_csv('card_following.csv', index = False)

    for uid in user_list[index:]:
        print(user_list.index(uid))
        print(uid)
        user_id = eval(uid)
        for uid in user_id:
            result_lst = following_scrape(uid)
            with open('card_following.csv', 'a') as f_object:
                writer_object = writer(f_object)
                for follow_id in result_lst:
                    writer_object.writerow([uid, follow_id])
                f_object.close()

# if can't find the index, run below two lines:
# tbl = pd.read_csv('card_following.csv')
# index = user_list.index("['sayedgolamrabbi8960']")

def follower_scrape(user_url):
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    URL = "https://www.behance.net/"+user_url
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    stats = soup.findAll('tr',{'class':'UserInfo-statRow-wH9'})
    try:
        if stats[-2].find('td').text == 'Followers':
            # locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
            num_followers = stats[-2].find('a').text
            if ',' in num_followers:
                num_followers = num_followers.replace(',','')
            num_followers = int(num_followers)
            print(num_followers)
    except:
        return ['']

    # launch the browser and go to the URL
    options = webdriver.ChromeOptions()
    options.add_argument('--blink-settings=imagesEnabled=false')
    options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
    options.add_argument('--headless=new')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=options)
    driver.get(URL)
    time.sleep(2)

    #locate the follower link: change this to following
    try:
        follower_button = driver.find_element(By.CSS_SELECTOR,'a.e2e-UserInfo-statValue-followers-count')
    except:
        return ['']
    driver.execute_script("arguments[0].click();", follower_button)
    time.sleep(2)
    users = driver.find_elements(By.CSS_SELECTOR,'li.Followers-profileRowItem-VI9')
    num_user = len(users)

    while True:
        try:
            driver.execute_script("arguments[0].scrollIntoView();", users[num_user-1] )
            time.sleep(2)
            new_users = driver.find_elements(By.CSS_SELECTOR,'li.Followers-profileRowItem-VI9')
            new_num_users = len(new_users)
            if new_num_users == num_user:
                break
            users = new_users
            num_user = new_num_users
   
        except:
            time.sleep(2)
            users = driver.find_elements(By.CSS_SELECTOR,'li.Followers-profileRowItem-VI9')
            num_user = len(users)
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    driver.close()
    driver.quit()

    followers = soup.find_all('a',{'class':'ProfileRow-profileLink-hvq e2e-ProfileRow-link'})
    followers_list = []
    for f in followers:
        followers_list.append(f['href'].split('/')[-1])
    return followers_list



def generate_follower_table(user_list, index):
    # if table is not intiated, create a new table using the two lines below
    # tbl = pd.DataFrame(columns = ['user_id', 'follower_id'])
    # tbl.to_csv('card_follower.csv', index = False)
    for user_id in user_list[index:]:
        print(user_list.index(user_id))
        print(user_id)
        user_ids = eval(user_id)
        for user_id in user_ids:
            print(user_id)
            result_lst = follower_scrape(user_id)
            with open('card_follower.csv', 'a') as f_object:
                writer_object = writer(f_object)
                for follow_id in result_lst:
                    writer_object.writerow([user_id, follow_id])
                f_object.close()
                
# if can't find the index, run below two lines:
# tbl = pd.read_csv('card_follower.csv')
# index = user_list.index("['paulrover']")