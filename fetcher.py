from selenium import webdriver
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import requests
from bs4 import BeautifulSoup


def fetch_vice_data():
    driver = webdriver.Chrome(executable_path='C:/Users/gaiters/Desktop/chromedriver.exe')
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
            # print(picture)
            img = picture['srcset']
            # print(img)

            images.append(img)
    driver.close()
    driver.quit()
        
    return titles, links, images


vice_data = fetch_vice_data()
titles_v = vice_data[0]
links_v = vice_data[1]
images_v = vice_data[2]

vice = {'titles': titles_v, 'links': links_v, 'images': images_v}

vice_data_df = pd.DataFrame.from_dict(vice, orient='index')
vice_data_df = vice_data_df.transpose()

pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)
print(vice_data_df)

    

    
