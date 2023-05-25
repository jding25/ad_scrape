from selenium import webdriver
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from adLinks import *
from projectScrape import *
import time
import re
import pandas as pd
import csv
from csv import writer
from readFile import *

# given user url, returns a list of user information on that user's web page, which contains:
#'user_id','user_name','user_occupation','user_location','website','featured','project_views','num_appreciations','num_followers','num_followings','bios','tool_list'

def user_info(userURL):
    options = webdriver.ChromeOptions()
    options.add_argument('--blink-settings=imagesEnabled=false')
    options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
    options.add_argument('--headless=new')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=options)

    # Navigate to a web page
    requests.get(userURL)
    driver.get(userURL)
    # if it has read more button, click the button
    try:
        read_more = driver.find_element('xpath',"/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/main[1]/div[2]/div[1]/div[2]/div[3]/div[2]/div[1]/div[1]/div[1]/a[1]")
        driver.execute_script("arguments[0].click();", read_more)
    except:
        pass

    # Scroll to the bottom of the page to load all content
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        try:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        except:
            break
    try:
        read_more = driver.find_element('xpath',"/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/main[1]/div[2]/div[1]/div[2]/div[3]/div[2]/div[1]/div[1]/div[1]/a[1]")
        driver.execute_script("arguments[0].click();", read_more)
    except:
        pass
    
    #Get the HTML of the fully-loaded page
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    # quit the selenium driver
    driver.quit()

    # find all the comments on the page
    comments = soup.find_all("a", {"class": "user-name-link bold e2e-comment-user-name-link"})

    user_url_list = []
    for comment in comments:
    # find the user URL in each comment
        user_url = comment['href']
        user_url_list.append(user_url)

    # find the basic of information of the user
    basic_info_list = []
    user_id = re.split('/',userURL)[-1]
    
    user_name = ""
    if soup.find("h1",{"class":"ProfileCard-userFullName-ule"}):
        user_name = soup.find("h1",{"class":"ProfileCard-userFullName-ule"}).contents
   
    user_occupation = ''
    if soup.find("p",{"class":"ProfileCard-line-fVO e2e-Profile-occupation"}):
        user_occupation = soup.find("p",{"class":"ProfileCard-line-fVO e2e-Profile-occupation"}).contents
 
    user_location = ""
    if soup.find('span', {'class':'e2e-Profile-location'}):
        user_location = soup.find('span', {'class':'e2e-Profile-location'}).contents
   
    website = ""
    if soup.find('p',{'class':'ProfileCard-line-fVO ProfileCard-anchor-q0M ProfileCard-lineText-Q4b'}):
        division = soup.find('p',{'class':'ProfileCard-line-fVO ProfileCard-anchor-q0M ProfileCard-lineText-Q4b'})
        if division.find('a', {"class":"ProfileCard-anchor-q0M"}):
            website = soup.find('a', {"class":"ProfileCard-anchor-q0M"}).contents

    featured = []
    if soup.find('img', {"class":"rf-ribbon__image Feature-ribbonImage-Ung"}):
        featurs = soup.find_all('img', {"class":"rf-ribbon__image Feature-ribbonImage-Ung"})
        for feature in featurs:
            featured.append(feature['alt'])

    bios = {}
    divs = soup.find_all('div',{'class':"UserInfo-infoBlockRow-jf1"})  
    for div in divs:
        try:
            if div.find('div',{'class':'UserInfo-bio-OZA'}):
                if div.find('div',{'class':'ReadMore-content-F2D'}):
                    bios['ABOUT US'] = div.find('div',{'class':'ReadMore-content-F2D'}).text
                else:
                    title = div.find('p',{'class':'UserInfo-rowTitle-MZz'}).text

                    bios[title] = div.find('div',{'class':'UserInfo-bio-OZA'}).find('span').text
        except:
            pass

    tool_list = []
    try:
        tools = soup.find_all('img',{'class':'ProjectTools-toolIcon-Sdh'}, alt=True)
        for tool in tools:
            tool_list.append(tool['alt'])
    except:
        pass
    basic_info_list.extend([user_id, user_name, user_occupation, user_location, website, featured])
    # find the number of likes on the page
    basic_info = soup.find_all("a", {"class": "UserInfo-statValue-d3q"})    
    #basic info list contains project views, number of appreciations, number of followers, and number of followings, in this order.
    extras = []
    for i in basic_info:
        extras.append(i.contents)
    if len(extras) != 4:
        for i in range(4 -len(extras)):
            extras.append([])
    basic_info_list.extend(extras)

    basic_info_list.extend([bios,tool_list])

    #retrieve work list and appreciation list
    project_links = soup.find_all('a', {'title': 'Link to project'})
    work_list = []
    # Loop through each project link and find the link to the project's image
    for link in project_links:
        try:
            project_url = link["href"]
            work_list.append(project_url)
        except:
            pass

    basic_info_list.append(work_list)
    return basic_info_list


# ad_url_list = []
# def saveWorkList():
#     with open('another_ad_list.csv', 'w') as f: 
#         csv_writer = csv.writer(f)
#         csv_writer.writerow(ad_url_list)

# generate/ append to user table given a list of user urls and the index at that user url list.
# exampe input: user_list = read_list('card_user_list'); index = 0
def generate_user_table(user_list, index):
    user_columns = ['user_id','user_name','user_occupation','user_location','website','featured','project_views','num_appreciations','num_followers','num_followings','bios','tool_list']

    #intialize a table for user info if there is not one already; comment the below two lines if there is already one intialized.
    tbl  = pd.DataFrame(columns = user_columns)
    tbl.to_csv('card_users.csv', index = False)
    # tbl = pd.read_csv('users.csv')
    for user_id in user_list[index:]:
        url = "https://www.behance.net/"+user_id[2:-2]
        result_lst = user_info(url)
        with open('card_users.csv', 'a') as f_object:
            writer_object = writer(f_object)
            writer_object.writerow(result_lst)
            f_object.close()













