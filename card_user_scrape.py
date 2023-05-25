import pandas as pd
from readFile import *


user_list = []
business_user_id_list = pd.read_csv('businesscard_work.csv').index.tolist()
credit_user_id_list = pd.read_csv('creditcard_work.csv').index.tolist()
post_user_id_list = pd.read_csv('postcard_work.csv').index.tolist()
ID_user_id_list = pd.read_csv('IDcard_work.csv').index.tolist()
product_user_id_list = pd.read_csv('productcard_work.csv').index.tolist()
gift_user_id_list = pd.read_csv('giftcard_work.csv').index.tolist()
user_list = business_user_id_list + credit_user_id_list + post_user_id_list  + product_user_id_list + gift_user_id_list + ID_user_id_list
print(user_list)

# remove duplicates
user_list = list(set(user_list))

write_list(user_list,'card_url_list')



