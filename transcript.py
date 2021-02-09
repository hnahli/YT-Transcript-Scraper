import bs4
from bs4 import BeautifulSoup
import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
import time
import random
import re

driver = webdriver.Chrome(executable_path=r'/Users/hnahli/Desktop/Projects/Youtube V1/chromedriver')
wait = WebDriverWait(driver, 10)
url = 'https://www.youtube.com/watch?v=OAygXmNwDOU'

def get_transcript(url):
    driver.get(url)
    time.sleep(2)
    driver.maximize_window()
    time.sleep(random.randint(5,10))
    js = driver.execute_script('return JSON.parse(ytplayer.config.args.player_response).captions.playerCaptionsTracklistRenderer.captionTracks[0].baseUrl')
    time.sleep(random.randint(1,5))
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
    script = str(transcripts[0]).replace('&#39;', "'")
    script = str(transcripts[0]).replace("&quot;", '"')

    return script
get_transcript(url)
print(get_transcript(url))