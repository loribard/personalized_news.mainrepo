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



def authorized():
	"""getting the args to be able to access the information from the path /authorize_callback"""


	state = request.args.get('state', '')
	code = request.args.get('code', '')
	# print code
	# code = 'bPIZoepShvTONoIoSAPPawOsmuI'
	info = r.get_access_information(code)
	return r.get_me() 
		


# interest='funny'
def get_subreddits_by_interest(interest):
	"""This returns the top five (limit) reddits for the interest chosen"""


	subreddit = r.get_subreddit(interest).get_top(limit=5)
	
	# print "TYPE", type(subreddit)
	i = 0
	subreddit_dict = {}
	subreddits = {}
	for item_of_interest in subreddit:
		# print item_of_interest.title
		# print item_of_interest.url
		title = item_of_interest.title
		url = item_of_interest.url
		subreddits[i] = {"title":title,"url":url}
		i+=1
		
	# subreddit_dict[interest] = subreddits
	# print "Dictionary of "+interest+": " +str(subreddit_dict)
	return subreddits



if __name__=="__main__":
	authorize = get_authorize_reddit_link()
	hop_into_api = authorized()
	get_subreddits_by_interest(interest)
