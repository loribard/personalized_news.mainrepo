
import json
import requests
URL="https://www.reddit.com/r/funny.json"

#we're fetching the url, decoding the json string, and then printing the titles of articles on the page.


def fetch_listing(url):
    response = requests.get(url)
    return response.text

def decode_listing_str(listing_str):
    listing_dict = json.loads(listing_str)
    return listing_dict

def print_titles(listing_dict):
    posts = listing_dict["data"]["children"]
    for post in posts:
        print post["data"]["title"]
        print post["data"]

def main():
    listing_str = fetch_listing(URL)
    listing_dict = decode_listing_str(listing_str)
    print_titles(listing_dict)

if __name__ == '__main__':
	main()