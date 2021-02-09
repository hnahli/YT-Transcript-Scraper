import bs4
from bs4 import BeautifulSoup
import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
import time
import random

driver = webdriver.Chrome(executable_path=r'/Users/hnahli/Desktop/Projects/Youtube V1/chromedriver')
wait = WebDriverWait(driver, 10)
url = 'https://www.youtube.com/channel/UCNjPtOCvMrKY5eLwr_-7eUg/videos'

def get_videos(url):
    driver.get(url)
    driver.maximize_window()
    time.sleep(2)

    for i in range(0,50):
        driver.execute_script("window.scrollBy(0,document.body.scrollHeight || document.documentElement.scrollHeight)", "")
        time.sleep(random.randint(5,15))

    html = driver.execute_script("return document.documentElement.outerHTML")
    soup = BeautifulSoup(html, 'html.parser')
    title_container = soup.find_all("a",{"class":"yt-simple-endpoint style-scope ytd-grid-video-renderer"})
    date__container = soup.find_all("span",{"class":"style-scope ytd-grid-video-renderer"})

    titles = []
    urls = []
    views = []
    dateold = []

    for title in title_container:
        titles.append(title.text)
    for i in range(0, len(date__container)):
        if (i % 2) == 0:
            views.append(date__container[i].text)
        else:
            dateold.append(date__container[i].text)

    for title in title_container:
        urls.append('https://youtube.com'+title["href"])

    #for i in range(0,len(titles)):
    #    print(urls[i] , ' | ', titles[i], ' | ',views[i], ' | ', dateold[i])

    df = pd.DataFrame(list(zip(urls, titles,views,dateold)), 
                columns =['Video URL', 'Title', 'Views', 'Date'])
    #mdf = df[df['Views'].str.contains('M')]
    mdf = df[df['Views'].str.contains('M')]

    mdf.to_csv(r'BestieVideosList.csv')
    return mdf
get_videos(url)