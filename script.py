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
url = 'https://www.youtube.com/channel/UC4rlAVgAK0SGk-yTfe48Qpw/videos'

def get_transcript(url):

    time.sleep(2)
    driver.get(url)
    time.sleep(2)
    driver.maximize_window()
    time.sleep(random.randint(10,25))
    js = driver.execute_script('return JSON.parse(ytplayer.config.args.player_response).captions.playerCaptionsTracklistRenderer.captionTracks[0].baseUrl')
    time.sleep(random.randint(10,25))
    driver.get(js)
    html = driver.execute_script("return document.documentElement.outerHTML")
    soup = BeautifulSoup(html, 'html.parser')
    cc = soup.findAll('text')
    time.sleep(2)
    transcripts = []

    #the_list[0] = f"{the_list[0]} a b c"
    for c in cc:
        transcripts.append(c.text)   
        transcripts[0] = f"{transcripts[0]}" + ' '+ c.text      
            
    return transcripts[0]


def get_videos(url):
    driver.get(url)
    driver.maximize_window()
    time.sleep(2)

    for i in range(0,25):
        driver.execute_script("window.scrollBy(0,document.body.scrollHeight || document.documentElement.scrollHeight)", "")
        time.sleep(random.randint(3,10))

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
    mdf = df[df['Views'].str.contains('M')]

    return mdf['Video URL']

#print(get_transcript((get_videos('https://www.youtube.com/channel/UC4rlAVgAK0SGk-yTfe48Qpw/videos')).iloc[0]))

column_names = ["URL", "Script"]
master_df = pd.DataFrame(columns = column_names)

for url in get_videos(url):

    master_df = master_df.append({'URL': url, 'Script': get_transcript(url)}, ignore_index=True)
    time.sleep(random.randint(15,35))
print(master_df)
master_df.to_csv(r'final.xlsx')