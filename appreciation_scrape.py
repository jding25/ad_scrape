import requests
from bs4 import BeautifulSoup
from adLinks import *
from projectScrape import *
import re
import pandas as pd
import numpy as np
from readFile import *

#given user id, return basic profile, a list of appreciations links, a list of work links
def appreacted_list(userURL):
    work_id_lst = []
    try:
        appreciated_list = all_links_of_divs('https://www.behance.net/'+userURL + "/appreciated", 'a','class','AppreciationCover-coverLink-x1o')
        for url in appreciated_list:
            work_id_lst.append(url.split('?')[0])
        user_url_lst = np.array([userURL.split('/')[-1]]*len(work_id_lst))
        df = pd.DataFrame({'user_id':user_url_lst,'appreciation_project_url': work_id_lst})
        return df
    except:
        pass

#example: user_list = read_list('card_user_list'), index = user_list.index("['sayedgolamrabbi8960']")
def generate_appreciation_table(user_list, index):
    # if a table not initiated, run the below two lines
    # tbl = pd.DataFrame(columns = ['user_id', 'appreciation_project_url'])
    # tbl.to_csv('card_appreciation.csv', index = False)

    for uid in user_list[index+1:]:
        print(user_list.index(uid))
        user_id = eval(uid)
        for uid in user_id:
            result_tbl = appreacted_list(uid)
            try:
                result_tbl.to_csv('card_appreciation.csv', mode='a', index=False, header=False)
                print(uid)
            except:
                print('error', uid)


    




