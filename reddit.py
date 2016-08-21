import json
import requests
import praw
import os
from flask import Flask, render_template, request, flash, redirect, session
from pprint import pprint




CLIENT_ID =  os.environ['CLIENT_ID']
CLIENT_SECRET = os.environ['CLIENT_SECRET']
REDIRECT_URI = 'http://127.0.0.1:65010/authorize_callback'

r = praw.Reddit('Test of Reddit API ')
r.set_oauth_app_info(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)

def get_authorize_reddit_link():
	"""getting reddit authorize link"""


	return r.get_authorize_url('DifferentUniqueKey',['identity', 'read', 'submit', 'history', 'report'],
									   refreshable=True)



def authorized(state, code):
	"""getting the args to be able to access the information from the path /authorize_callback"""

	info = r.get_access_information(code)
	return r.get_me() 
		


# interest='funny'
def get_subreddits_by_interest(interest):
    """This returns the top five (limit) reddits for the interest chosen"""


    subreddit = r.get_subreddit(interest).get_top(limit=5)

    
    subreddits = {}
    
    i=0
    
    for item_of_interest in subreddit:
        title = item_of_interest.title
        url = item_of_interest.url

        # data_to_look_at = str(url)+ '/.json'
        # data=data_to_look_at.json()
        # print data
        # json.dumps(data_to_look_at)
        # f=open('data_to_look_at.json','w')
        # f.write(json.dumps(data_to_look_at))
        # f.close
        # f=open('data_to_look_at.json')
        # data=f.read()
        # result=json.loads(data)
        # print '###################'
        # print result
        # print '********************'

        # import pdb; pdb.set_trace()
        thumbnail = item_of_interest.thumbnail
        more=item_of_interest.replace_more_comments

        
        subreddits[i] = {"title":title,"url":url,"thumbnail":thumbnail}
        i+=1
        
       
        
   
    return subreddits

    def look_at_data(json_file):
        r = requests.get(json_file)
        data = r.json()
        keys = data.keys()
        print keys
        return




 		# subreddits_dig_deeper = {}
 		# import pdb; pdb.set_trace()
 		 # more_info = item_of_interest.replace_more_comments(limit=None,threshold=0)
 		 # subreddits_dig_deeper[i] = more_info

 	

 	

 
 	
 	# for item in data['data']['children']:
 	# 	print '*********************'
 	# 	print item['data']['preview']['images'][0]['source']['url']

 #                for k in keys:
 #                    d = d.get(v, {})
 #                if d:
 #                    return d

 #            image_url = find_key(post, ["preview", "images", "0", "source", "url"])
 #            if image_url:
 #                ...
	# subreddit_urls = {}
	# for item_of_interest in subreddit:


if __name__=="__main__":
	authorize = get_authorize_reddit_link()
	hop_into_api = authorized()
	get_subreddits_by_interest(interest)
