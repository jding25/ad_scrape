import pandas as pd
from scrollProjectPage import *
from projectScrape import *
from csv import writer

IDcard = pd.read_csv('IDcard.csv')

work_columns = ['project_url','project_id', 'user_id', 'title', 'published_time', 'num_likes', 'num_views', 'num_comments', 'tags_list','license', 'text', 'permalnks']
# #comment_columns = ['user_id','work_id','time','contents']

work_data = pd.DataFrame(columns = work_columns)
# #comment_data = pd.DataFrame(columns = comment_columns)
work_data.to_csv('IDcard_work.csv',index = False)



for i in range(IDcard.shape[1]):
    print(i)
#     #modify links
    link = IDcard.columns[i].replace("'","").split("?")[0]
    curr_html = scrollPage(link)
    curr = get_commenturl_likes_views(link, curr_html)
    with open('IDcard_work.csv', 'a') as f_object:
        # Pass this file object to csv.writer()
        # and get a writer object
        writer_object = writer(f_object)
        # Pass the list as an argument into
        # the writerow()
        writer_object.writerow(curr)
        # Close the file object
        f_object.close()