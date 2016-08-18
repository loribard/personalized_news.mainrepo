import praw
import os
from flask import Flask, render_template, request, flash, redirect, session



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
	
	i=0
	subreddits = {}

	for item_of_interest in subreddit:
		title = item_of_interest.title
		# import pdb; pdb.set_trace()
		url = item_of_interest.url
		print item_of_interest.thumbnail,'###################################'
		subreddits[i] = {"title":title,"url":url}
		i+=1

	

		

		
	return subreddits



	

	# def find_key(d, keys):
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
