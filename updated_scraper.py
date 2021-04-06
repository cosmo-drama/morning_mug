import requests
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup
from newsapi import NewsApiClient
import json
import config

api_key = config.api_key
newsapi = NewsApiClient(api_key)

# articles we can get from news_api
vox_media = 'https://newsapi.org/v2/everything?domains=%s&pageSize=3&apiKey=%s' % ('vox.com', api_key)
the_verge = 'https://newsapi.org/v2/everything?domains=%s&pageSize=3&apiKey=%s' % ('theverge.com', api_key)
pitchfork = 'https://newsapi.org/v2/everything?domains=%s&pageSize=3&apiKey=%s' % ('pitchfork.com', api_key)
wsj = 'https://newsapi.org/v2/everything?domains=%s&pageSize=3&apiKey=%s' % ('wsj.com', api_key)
nasa = 'https://newsapi.org/v2/everything?domains=%s&pageSize=3&apiKey=%s' % ('nasa.gov', api_key)
associated_press = 'https://newsapi.org/v2/everything?domains=%s&pageSize=3&apiKey=%s' % ('apnews.com', api_key)
wired = 'https://newsapi.org/v2/everything?domains=%s&pageSize=3&apiKey=%s' % ('wired.com', api_key)
ny_mag = 'https://newsapi.org/v2/everything?domains=%s&pageSize=3&apiKey=%s' % ('nymag.com', api_key)
the_atlantic = 'https://newsapi.org/v2/everything?domains=%s&pageSize=3&apiKey=%s' % ('theatlantic.com', api_key)
itsnicethat = 'https://newsapi.org/v2/everything?domains=%s&pageSize=3&apiKey=%s' % ('itsnicethat.com', api_key)

sources = [vox_media, the_atlantic, the_verge, pitchfork, wsj, nasa, associated_press, wired, ny_mag, itsnicethat]

def fetch_data(source):
    source_response = requests.get(source)
    source_content = source_response.json()
    
    print('Content from %s scraped successfully.' % source)

    return source_content

def save_data(source_content):
    sourced = source_content['articles'][0]
    source_name = sourced['source']['name']
    
    with open('/home/athena/projects/morning_mug/data/%s' % source_name + '.json', 'w') as f:
        json.dump(source_content, f)
        print('%s.json file created' % source_name)


for source in sources:
    source_content = fetch_data(source)
    save_data(source_content)

