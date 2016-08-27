import json
import os
import urllib3.contrib.pyopenssl
urllib3.contrib.pyopenssl.inject_into_urllib3()
import certifi
import urllib3
http = urllib3.PoolManager(
    cert_reqs="CERT_REQUIRED",
    ca_certs=certifi.where())

api = os.environ.get('API') 


def get_headlines(newssource):
    """using newsapi, fetch the top of the news from the specified newssource"""
 
    newssource_dict = {}
    url = 'https://newsapi.org/v1/articles?source=' + newssource + '&sortBy=top&apiKey=' + api
    request = http.request('GET',url,timeout=4.0)

    headline = json.loads(request.data)
    print headline
    newssource_dict['url'] = headline['articles'][0]['url']
    newssource_dict['title']= headline['articles'][0]['title']
    newssource_dict['description'] = headline['articles'][0]['description']
   
    
    return newssource_dict






