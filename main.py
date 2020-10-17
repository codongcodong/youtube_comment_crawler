# -*- coding: utf-8 -*-

from selenium import webdriver as wd
from bs4 import BeautifulSoup
import time
from collections import defaultdict

def crawl_youtube_page_html_source(url):

    driver = wd.Chrome(executable_path="./chromedriver")
    driver.implicitly_wait(3)
    driver.get(url)

#scrolling to the end of page

    last_page_height = driver.execute_script("return document.documentElement.scrollHeight")

    for i in range(2):
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight/4);")
        time.sleep(3.0)

    while True:
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        time.sleep(4.0)
        new_page_height = driver.execute_script("return document.documentElement.scrollHeight")

        if new_page_height == last_page_height:
            time.sleep(4.0)    #giving second chance in case of slow page load
            new_page_height = driver.execute_script("return document.documentElement.scrollHeight")

            if new_page_height == last_page_height:
                time.sleep(4.0)  # giving thrid chance in case of slow page load
                new_page_height = driver.execute_script("return document.documentElement.scrollHeight")

                if new_page_height == last_page_height:
                    break

        last_page_height = new_page_height

    print("Scrolling complete, clicking buttons to load replies...")

#clicking reply buttons

    css_selector = 'paper-button#button.style-scope.ytd-button-renderer'
    buttons = driver.find_elements_by_css_selector(css_selector)
    
    dapgle = u'답글'
    bogi = u'보기'
    
    for button in buttons:
        if dapgle in button.text and bogi in button.text:
            driver.execute_script("arguments[0].scrollIntoView();", button)
            driver.execute_script("arguments[0].click();", button)
            time.sleep(2.0)

    html_source = driver.page_source
    print("Got html source")

    driver.quit()
    return html_source

def get_timestamps(file, html):
    timestamps_stats = defaultdict(int)
    soup = BeautifulSoup(html, 'lxml')

    youtube_timestamps = soup.select('a.yt-simple-endpoint.style-scope.yt-formatted-string')

    youtube_comments = soup.select('yt-formatted-string#content-text')

    file.write("# of crawled comments: %d\n"%len(youtube_comments))
    print("Parsing timestamps")

    for timestamp in youtube_timestamps:
        time_value = parse_timestamp(timestamp.text)

        if time_value != -1:
            timestamps_stats[time_value] += 1

    return timestamps_stats

def parse_timestamp(s):
    tokens = s.split(':')
    l = len(tokens)
    res = 0

    if l==2:        #00:00~59:59
        for i in range(2):
            if tokens[i].isdigit() and len(tokens[i])<=2:
                temp = int(tokens[i])
                if temp >= 60 or temp < 0:
                    return -1
                if i == 0:  #minute
                    res += (temp*60)
                else:       #second
                    res += temp
            else:
                return -1

    elif l==3:      #00:00:00~99:59:59
        for i in range(3):
            if tokens[i].isdigit() and len(tokens[i]) <= 2:
                temp = int(tokens[i])
                if i==0:        #hour
                    if temp >= 100 or temp < 0:
                        return -1
                    res += (temp*3600)
                else:
                    if temp >= 60 or temp < 0:
                        return -1
                    if i == 1:  # minute
                        res += (temp * 60)
                    else:  # second
                        res += temp
            else:
                return -1
    else:
        return -1

    return res

def print_statistics(file,stats):
    k = list(stats.keys())
    k.sort()

    for time_value in k:
        if time_value < 3600:
            file.write("%02d:%02d - %d\n"%(time_value//60, time_value%60, stats[time_value]))
        else:
            file.write("%d:%02d:%02d - %d\n"%(time_value // 3600, (time_value % 3600) // 60, time_value % 60, stats[time_value]))

url = 'https://www.youtube.com/watch?v=JyrFhfjwfDo&ab_channel=tvN'
#url = 'https://www.youtube.com/watch?v=0UKwpJUUDlM&ab_channel=essential%3B' #Avengers 명장면
url = 'https://www.youtube.com/watch?v=a-3tU8r7rMw'

if __name__=="__main__":

    urls = [url]

    for i in range(1):
        print("anaylzing url%d: %s"%(i,urls[i]))
        for j in range(3):
            output_file = open('url%d-%d.txt'%(i,j),'w')
            output_file.write('url: '+urls[i]+'\n')

            html_source = crawl_youtube_page_html_source(urls[i])
            timestamps_stats = get_timestamps(output_file,html_source)
            print_statistics(output_file,timestamps_stats)

            print("url%d %dth analysis complete"%(i,j))
