## userScrape.py
### function: `user_info` 
### input: user url
### output: a list of user information, including
###'user_id','user_name','user_occupation','user_location','website','featured','project_views','num_appreciations','num_followers','num_followings','bios','tool_list'
### function: `generate_user_table`
### input: user_list (a list of user urls), index(the current position on that list)
### output: generate a new user table by calling user_info for each user url on the user url list or appending to exisiting user table.

## scrollProjectPage.py
### function: `scrollPage`
### input: projectURL
### output: the html of the full page after scrolling down to the bottom of page (including clicking the load more button)

## projectScrape.py
### function: `get_commenturl_likes_views`
### input: projectURL, html [`scrollPage(projectURL)`]
### output: a list of information of the project page, including cleanedProjectURL,project_id, user_id, title, published_time, likes, views, num_comments, tags_list,license, text, permalnks, user_url_list
### function: `generate_project_comments_tables`
### input: project_list, index
### output: generate the project table and comment table

## readFile.py
### function: `write_list`
### input: list, filename
### output: the list will be stored as a binary file under the path decribed by filename
### function: `read_list`
### input: list_name
### output: convert the binary list back.

## adLinks.py
### function: `all_links_of_divs`
### input: url, div_type, inner_type, ad_class_name
### output: return a list of href links on that url that has this div_type, inner_type, and ad_class_name

## image_scrape.py
### function: `all_links_of_images`, a speicifc case usage of `all_links_of_divs`
### input: url
### output: a list of urls of images on that url page.

## following.py
### function: `following_scrape`
### input: user_url
### output: a list of users that the given user_url is following
### function: `generate_following_table`
### input: user_list, index
### output: generate/append to a table that calls `following_scrape` on each url on the url list
### function: `follower_scrape`
### input: user_url
### output: a list of users that the given user_url is followed
### function: `generate_follower_table`
### input: user_list, index
### output: generate/append to a table that calls `generate_follower_table` on each url on the url list

## comment_scrape.py
### function: `get_comment_contents`
### input: projectURL
### output: a table that contrians all the comments for a given project url.

## appreciation_scrape.py
### function `appreciated_list`
### input: userURL
### output: the list of appreciated works by the given userURL
### function: `generate_appreciation_table`
### input: user_list, index
### output: append to/generate appreciation table by running `appreciated_list` on the url list.

all the file that end with _work_scrape.py or card_scrape.py (such as product_work_scrape, post_work_scrape, and id_card_scrape) are used to scrape projects for specific cards types on Behance.net. 
