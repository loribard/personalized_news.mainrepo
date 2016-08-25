import json
import requests
import praw
import os
from flask import Flask, render_template, request, flash, redirect, session
from pprint import pprint




CLIENT_ID =  os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
REDIRECT_URI = 'http://127.0.0.1:65010/authorize_callback'

if not (CLIENT_ID and CLIENT_SECRET):
    raise Exception("I need a CLIENT_ID and CLIENT_SECRET")

r = praw.Reddit('Test of Reddit API ')
r.set_oauth_app_info(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)
# import pdb; pdb.set_trace()

def get_authorize_reddit_link():
    """getting reddit authorize link"""
    return r.get_authorize_url('uniqueKey',['identity', 'read'],
                                       refreshable=True)


# interest='funny'
def get_posts_by_interest(interest):
    """This returns the top five (limit) reddits for the interest chosen"""


    subreddit = r.get_subreddit(interest).get_top(limit=5)
    
    # r=requests.get('https://www.reddit.com/r/funny.json')
    # data=r.json()

    
    posts = []
        
    for praw_post in subreddit:
        post = {"title": praw_post.title,
                "url": praw_post.url,
                "thumbnail": praw_post.thumbnail}

        if hasattr(praw_post, "preview"):
            preview_image = praw_post.preview['images'][0]['source']['url']
        else:
            preview_image = None
        
        post["preview_image"] = preview_image
        posts.append(post)

    return posts

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
    #   print '*********************'
    #   print item['data']['preview']['images'][0]['source']['url']

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