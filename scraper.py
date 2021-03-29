import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
from bs4 import BeautifulSoup
from newsapi import NewsApiClient
import json
import config

def pitch_data(url, title_tag, link_tag, image_tag):
    url_r = requests.get(url)
    url_content = url_r.content

    soup = BeautifulSoup(url_content, features="html.parser")

    url_elements_h2 = soup.find_all('h2', class_=title_tag)
    url_elements_a2 = soup.find_all('a', class_=link_tag)

    titles = []
    links = []
    images = []

    for i in url_elements_h2:
        title_text = i.get_text()
        titles.append(title_text)

    for i in url_elements_a2:
        link = i.get('href')        
        link = url + link

        links.append(link)
    
    for i in links:
        i_response = requests.get(i)
        i_link = i_response.content
        soup_i = BeautifulSoup(i_link, features="html.parser")
        url_elements_img = soup_i.find_all('img', image_tag )
        
        img = url_elements_img

        for i in img:
            image = i['src']
            if image.startswith('https:') is True:
                images.append(image)

    return titles, links, images
    

def nice_data(url, title_tag, link_tag, image_tag):
    url_r = requests.get(url)
    url_content = url_r.content

    soup = BeautifulSoup(url_content, features="html.parser")

    url_elements_title = soup.find_all('span', class_=title_tag)
    url_elements_link = soup.find_all('a', class_=link_tag)

    titles = []
    links = []
    images = []

    for i in url_elements_title:
        title = i.get_text()
        titles.append(title)
    

    for i in url_elements_link:
        link = i.get('href')
        link = url + link
        
        links.append(link)
        
        link_response = requests.get(link)
        link_content = link_response.content
        soup_link = BeautifulSoup(link_content, features="html.parser")

            
        url_elements_img = soup_link.find('img')
        img = url_elements_img
           
        image = img.get('src')
        images.append(image)


    return titles, links, images


def fetch_vice_data():
    # driver = webdriver.Chrome('/usr/bin/chromedriver')
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")

    chrome_driver_location = "/home/sphinx/projects/morning_mug/venv/venv/bin/chromedriver"

    driver = webdriver.Chrome(chrome_driver_location, options=chrome_options)
    driver.get('https://vice.com/en/section/news')

    driver.execute_script("window.scrollTo(0, 200000);")
    driver.implicitly_wait(10)
    driver.find_elements_by_id('35 85313014-a-920651-bf-8-c-0-cfb')

    title_elements_a = driver.find_elements_by_class_name('vice-card-hed__link')
    titles = []
    links = []
    images = []

    for i in title_elements_a:

        title = i.text


        titles.append(title)

        link = i.get_attribute('href')

        links.append(link)
        link_r = requests.get(link)
        link_content = link_r.content

        soup = BeautifulSoup(link_content, features="html.parser")

        url_elements_img = soup.select('picture')
        for i in url_elements_img:
            picture = i.source
            img = picture['srcset']

            images.append(img)
    driver.close()
    driver.quit()
        
    return titles, links, images


api_key = config.api_key
# init

newsapi = NewsApiClient(api_key)
top_headlines_ars = newsapi.get_top_headlines(sources='ars-technica', language='en')
top_headlines_verg = newsapi.get_top_headlines(sources='the-verge', language='en')
top_headlines_wired = newsapi.get_top_headlines(sources='wired', language='en')


sources = "the-verge, ars-technica, wired"
selected = newsapi.get_top_headlines(sources=sources, language='en')


the_verge = top_headlines_verg
the_verge = the_verge['articles']
ars = top_headlines_ars
ars = top_headlines_ars['articles']
wired = top_headlines_wired
wired = wired['articles']

the_verge = json.dumps(the_verge, indent=2)
the_verge = json.loads(the_verge)
the_verge_df = pd.json_normalize(the_verge)

ars = json.dumps(ars, indent=2)
ars = json.loads(ars)
ars_df = pd.json_normalize(ars)

wired = json.dumps(wired, indent=2)
wired = json.loads(wired)
wired_df = pd.json_normalize(wired)


# pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)
# pd.set_option('display.max_colwidth', None)





# print(the_verge)
# verge_df = pd.DataFrame(the_verge)
# ars_df = pd.DataFrame(ars)
# wired_df = pd.DataFrame(wired)



vice_data = fetch_vice_data()
itsnicethat_data = nice_data('https://itsnicethat.com', 'listing-item-title', 'block link-reset py4 px4 sm-px4 md-px3 lg-px4', 'bg-white')
pitchfork_data = pitch_data('https://pitchfork.com', 'title module__title','title-link module__title-link', 'responsive-image__image')


titles_v = vice_data[0]
links_v = vice_data[1]
images_v = vice_data[2]

titles_p = pitchfork_data[0]
links_p = pitchfork_data[1]
images_p = pitchfork_data[2]

titles_n = itsnicethat_data[0]
links_n = itsnicethat_data[1]
images_n = itsnicethat_data[2]

vice = {'titles': titles_v, 'links': links_v, 'images': images_v}
pitchfork = {'titles': titles_p, 'links': links_p, 'images': images_p}
itsnicethat = {'titles': titles_n, 'links': links_n, 'images': images_n}

vice_data_df = pd.DataFrame.from_dict(vice, orient='index')
vice_data_df = vice_data_df.transpose().dropna()

pitchfork_df = pd.DataFrame.from_dict(pitchfork, orient='index')
pitchfork_df = pitchfork_df.transpose().dropna()

itsnicethat_df = pd.DataFrame.from_dict(itsnicethat, orient='index')
itsnicethat_df = itsnicethat_df.transpose().dropna()

# pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)
# pd.set_option('display.max_colwidth', None)
# pd.set_option('display.max_rowwidth', -1)

# print(pitchfork_df)
# print('\n\n')
# print(itsnicethat_df)
# print('\n\n')
# print(vice_data_df.dropna())
