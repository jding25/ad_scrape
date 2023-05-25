from selenium import webdriver
import requests
from bs4 import BeautifulSoup
import time
import re 
from scrollProjectPage import *
from readFile import *
from comment_scrape import *
import pandas as pd
import csv
from csv import writer
from scrollProjectPage import *
import numpy as np

# given a url of a project page, and the html of the full page by calling scrollPage(projectURL), retrieves all information on that project page, includincleanedProjectURL,project_id, user_id, title, published_time, likes, views, num_comments, tags_list,license, text, permalnks, user_url_list
def get_commenturl_likes_views(projectURL, html):
    soup = BeautifulSoup(html, "html.parser")
    text = ""
    if soup.find('h2',{"class":"ProjectInfo-projectDescription-dNH"}):
        text = soup.find('h2',{"class":"ProjectInfo-projectDescription-dNH"}).contents

    # find all the comments on the page
    comments = ""
    user_url_list = []
    if soup.find("a", {"class": "user-name-link bold e2e-comment-user-name-link"}):
        comments = soup.find_all("a", {"class": "user-name-link bold e2e-comment-user-name-link"})
        for comment in comments:
        # find the user URL in each comment
            user_url = comment['href']
            user_url_list.append(user_url)


    #find the title of the project
    title = ""
    if soup.find("span", {"class": "Project-title-Q6Q"}):
        title = soup.find("span", {"class": "Project-title-Q6Q"}).text
    #find the published time of the project
    published_time = ""
    if soup.find("div", {"class": "Project-projectPublished-X5a"}):
        published_time = soup.find("div", {"class": "Project-projectPublished-X5a"}).find('time').text
    # find the number of likes on the page
    likes = 0
    if soup.find("div", {"class": "ProjectInfo-projectStat-xLj beicons-pre beicons-pre-thumb e2e-ProjectInfo-projectStat-appreciations"}):
        likes = soup.find("div", {"class": "ProjectInfo-projectStat-xLj beicons-pre beicons-pre-thumb e2e-ProjectInfo-projectStat-appreciations"}).find('span')['title']
    # find the number of views on the page
    views = 0
    if soup.find("div", {"class":"ProjectInfo-projectStat-xLj beicons-pre beicons-pre-eye"}):
        views = soup.find("div", {"class":"ProjectInfo-projectStat-xLj beicons-pre beicons-pre-eye"}).find('span')['title']
    # find the number of comments of the project
    num_comments = 0
    if soup.find("div",{"class":"ProjectInfo-projectStat-xLj beicons-pre beicons-pre-comment qa-project-comment-count"}):
        num_comments = soup.find("div",{"class":"ProjectInfo-projectStat-xLj beicons-pre beicons-pre-comment qa-project-comment-count"}).text
    user_id = []
    # if it's multiple owner:
    if soup.find("div", {"class":"MultipleOwners-arrow-czw"}):
        user_id = []
        divs = soup.find_all("div",{"class":"ProjectInfo-infoBlocks-jRx ProjectInfo-profileInfo-T7a"})
        for divv in divs:
            if divv.find("h2",{"class":"SectionHeader-root-Qes UserInfo-header-jP0"}):
                heading = divv.find("h2",{"class":"SectionHeader-root-Qes UserInfo-header-jP0"}).contents
                if "Owners" in heading:
                    owners = divv.find_all("a",{"class":"UserInfo-userName-BoH qa-user-link e2e-ProjectOwnersInfo-user-link"})
                    for owner in owners:
                        user_id. append(re.split('/',owner['href'])[-1])
        
    else:
        if soup.find("a",{"class":"Avatar-avatar-G8t Avatar-avatarHover-z4f"}):
            user = soup.find("a",{"class":"Avatar-avatar-G8t Avatar-avatarHover-z4f"})['href']
            user_id.append(re.split('/',user)[-1])

    # find the list of tags
    tags_list = []
    if soup.find('li',{'class':"ProjectTags-tag-MKN"}):
        tags = soup.find_all('li',{'class':"ProjectTags-tag-MKN"})
        for tag in tags:
            tags_list.append(tag.text)
    # retrieve the url of all images on that project page
    permalnks = []
    if soup.find ('img',{"class": "ImageElement-image-SRv"}):
        permalinks = soup.find_all('img',{"class": "ImageElement-image-SRv"})
        for link in permalinks:
            permalnks.append(link['src'])

    project_id = re.findall("\d+",projectURL)[0]

    if (soup.find('img',{"class":"Copyright-copyrightIcon-sRr"})):
        license = soup.find('img',{"class":"Copyright-copyrightIcon-sRr"})['alt']
    else:
        license = "All Rights Reserved"
    cleanedProjectURL  =projectURL.split('?')[0]
    final_list = [cleanedProjectURL,project_id, user_id, title, published_time, likes, views, num_comments, tags_list,license, text, permalnks, user_url_list ]
    return final_list

#given a list of project url that's pregenerated, and the index of last url pm the list, continue adding to the table; or intialize a new table.
#example input: project_list = read_list("finished_10k_id"); index = 15397
def generate_project_comments_tables(project_list, index):
    # name the columns of the resulting project table
    project_columns = ['project_url','project_id', 'user_id', 'title', 'published_time', 'num_likes', 'num_views', 'num_comments', 'tags_list','license', 'text', 'permalnks']
    # name the columns of the resulting comment table
    comment_columns = ['user_id','work_id','time','contents']


    #intialize the table if not initialize before, comment out the below four lines if generated already
    project_tbl  = pd.DataFrame(columns = project_columns)
    comment_tbl = pd.DataFrame(columns = comment_columns)
    project_tbl.to_csv('10k_project.csv', index = False)
    comment_tbl.to_csv('10k_comment.csv', index = False)

    for project_id in project_list[index:index+10]:
        curr_html = scrollPage(project_id)
        project_result = get_commenturl_likes_views(project_id, curr_html)
        comment_table = get_comment_contents(project_id)
        with open('10k_project.csv', 'a') as f_object:
            writer_object = writer(f_object)
            writer_object.writerow(project_result)
            f_object.close()
        comment_table.to_csv('10k_comment.csv',mode='a', index=False, header=False)
        print(np.where(project_list==project_id)[0])