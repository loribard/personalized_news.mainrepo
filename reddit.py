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



def get_posts_by_interest(interest, limit=3):
    """This returns the top five (limit) reddits for the interest chosen
        >>> get_posts_by_interest("funny")
        3
        """



    subreddit = r.get_subreddit(interest).get_top(limit=limit)   
    posts = []
        
    for praw_post in subreddit:
        thumbnail = get_thumbnail(praw_post.thumbnail)
        post = {"title": praw_post.title,
                "url": praw_post.url,
                "thumbnail": thumbnail}


        if hasattr(praw_post, "preview"):
            preview_image = praw_post.preview['images'][0]['source']['url']
        else:
            preview_image = None
        
        post["preview_image"] = preview_image
        posts.append(post)

    print len(posts)
    return get_posts(posts)

def get_posts(posts):


    return posts

def get_thumbnail(thumbnail):
    """test to make sure the thumbnail is legitmate

        >>> get_thumbnail("default")
        ''
        >>> get_thumbnail("http://www.google.com")
        'http://www.google.com'
    """

    if thumbnail in ["default","self","nsfw",""]:
        thumbnail = ""
    return thumbnail



if __name__=="__main__":
    authorize = get_authorize_reddit_link()
    hop_into_api = authorized()
    get_subreddits_by_interest(interest)