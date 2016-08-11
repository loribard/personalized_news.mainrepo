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
	info = r.get_access_information(code)
	return r.get_me() 
	    


# interest='funny'
def get_subreddits_by_interest(interest):

    subreddit = r.get_subreddit(interest).get_top(limit=5)
    
    print "TYPE", type(subreddit)
    i = 0
    subreddit_dict = {}
    subreddits = {}
    for thing in subreddit:
        print thing.title
        print thing.url
        title = thing.title
        url = thing.url
        subreddits[i] = {"title":title,"url":url}
        i+=1
        
    print subreddits
    subreddit_dict[interest] = subreddits
    print subreddit_dict
    return subreddit_dict



if __name__=="__main__":
	authorize = get_authorize_reddit_link()
	hop_into_api = authorized()
	get_subreddits_by_interest(interest)
