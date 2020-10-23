# -*- coding: utf-8 -*-

from selenium import webdriver as wd
from bs4 import BeautifulSoup
import time
from collections import defaultdict

class video_url:
    def __init__(self, url, info, filename):
        self.url = url
        self.info = info
        self.filename = filename

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
        time.sleep(2.0)
        new_page_height = driver.execute_script("return document.documentElement.scrollHeight")

        if new_page_height == last_page_height:
            time.sleep(2.0)    #giving second chance in case of slow page load
            new_page_height = driver.execute_script("return document.documentElement.scrollHeight")

            if new_page_height == last_page_height:
                time.sleep(2.0)  # giving thrid chance in case of slow page load
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
        try:
            driver.execute_script("arguments[0].scrollIntoView();", button)
            button_text = button.text
        except:
            print("Error while getting button_text")
            driver.quit()
            return

        if dapgle in button_text and bogi in button_text:
            try:
                driver.execute_script("arguments[0].click();", button)
            except:
                print("Error while clicking buttons")
                driver.quit()
                return

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

#url = 'https://www.youtube.com/watch?v=JyrFhfjwfDo&ab_channel=tvN'
#url = 'https://www.youtube.com/watch?v=0UKwpJUUDlM&ab_channel=essential%3B' #Avengers 명장면
#url = 'https://www.youtube.com/watch?v=a-3tU8r7rMw'

testcase = video_url("https://www.youtube.com/watch?v=a-3tU8r7rMw","testcase","testcase")

#Big Buck Bunny
bunny0 = video_url("https://www.youtube.com/watch?v=YE7VzlLtp-4","big buck bunny original version - #C 2415","bunny0")
bunny1 = video_url("https://www.youtube.com/watch?v=aqz-KE-bpKQ","bug buck bunny 4k version - #C 3073","bunny1")

#3 pixar sparkshots

smashNgrab = "https://www.youtube.com/watch?v=A4-G7YpSFb4&list=PLpVg7pgd-JzP-DWROTsaMY8IDWElHMycx"
purl =  "https://www.youtube.com/watch?v=B6uuIHpFkuo&list=PLpVg7pgd-JzP-DWROTsaMY8IDWElHMycx"
kitbull = "https://www.youtube.com/watch?v=AZS5cgybKcI&list=PLpVg7pgd-JzP-DWROTsaMY8IDWElHMycx"

pixar1 = video_url(smashNgrab, "pixar sparkshots: smashNgrab, #C = 4259", "pixar1")
pixar2 = video_url(purl, "pixar sparkshots: purl, #C = 25843", "pixar2")
pixar3 = video_url(kitbull, "pixar sparkshots: kitbull, #C = 82893", "pixar3")

#5 National Geographic Short Film Showcase
#재생목록에서 댓글 수 일정 개수 이상인 동영상 위에서부터 5개

iceland = "https://www.youtube.com/watch?v=pnRNdbqXu1I&list=PLivjPDlt6ApTDlm7OufY6HAzNmFAqxWSo"
sahara = "https://www.youtube.com/watch?v=jEo-ykjmHgg&list=PLivjPDlt6ApTDlm7OufY6HAzNmFAqxWSo"
lost_african = "https://www.youtube.com/watch?v=B_a1WS5ncDk&list=PLivjPDlt6ApTDlm7OufY6HAzNmFAqxWSo"
salamander = "https://www.youtube.com/watch?v=SEejivHRIbE&list=PLivjPDlt6ApTDlm7OufY6HAzNmFAqxWSo"
underwater = "https://www.youtube.com/watch?v=L4qM1IEhtNQ&list=PLivjPDlt6ApTDlm7OufY6HAzNmFAqxWSo"

docu1 = video_url(iceland,"Iceland Is Growing New Forests #C=4137","docu1")
docu2 = video_url(sahara,"This Sahara Railway Is One of the Most Extreme in the World #C=4797","docu2")
docu3 = video_url(lost_african,"Inside a Lost African Tribe Still Living in India Today #C=6053","docu3")
docu4 = video_url(salamander,"See a Salamander Grow From a Single Cell #C = 14645","docu4")
docu5 = video_url(underwater,"Experience the Underwater World #C = 35191","docu5")

#5 Football
#Game Highlights(week5) | NFL 2020 위에서부터 5개

nfl1 = "https://www.youtube.com/watch?v=rPMLyYNigAk&list=PLRdw3IjKY2gmc-KBvUgfnlnw2n_RZ8Imf&index=5&ab_channel=NFL"
nfl2 = "https://www.youtube.com/watch?v=cXzlc-iKfEQ&list=PLRdw3IjKY2gmc-KBvUgfnlnw2n_RZ8Imf&index=1&ab_channel=NFL"
nfl3 = "https://www.youtube.com/watch?v=1YIigArbYoo&list=PLRdw3IjKY2gmc-KBvUgfnlnw2n_RZ8Imf&index=3&ab_channel=NFL"
nfl4 = "https://www.youtube.com/watch?v=eujFTIUuMYs&list=PLRdw3IjKY2gmc-KBvUgfnlnw2n_RZ8Imf&index=4&ab_channel=NFL"
nfl5 = "https://www.youtube.com/watch?v=V5HqqFu4sfA&list=PLRdw3IjKY2gmc-KBvUgfnlnw2n_RZ8Imf&index=6&ab_channel=NFL"

sport1 = video_url(nfl1,"Colts vs. Browns #C = 2950","nfl1")
sport2 = video_url(nfl2,"Bills vs. Titans #C = 4203","nfl2")
sport3 = video_url(nfl3,"Vikings vs. Seahawks #C = 6153","nfl3")
sport4 = video_url(nfl4,"Giants vs. Cowboys #C = 4864","nfl4")
sport5 = video_url(nfl5,"Dolphins vs. 49ers #C = 3210","nfl5")


#Doctor Who: COMPILATIONS
#Friends: TBS clip

doctor1 = "https://www.youtube.com/watch?v=TtfG0QLjM_E&list=PLKEzuOOEQvYM4TKmECNOrGgsrRGvM9-dA&index=3&ab_channel=DoctorWho"
doctor2 = "https://www.youtube.com/watch?v=mcggi9kXiaY&list=PLKEzuOOEQvYM4TKmECNOrGgsrRGvM9-dA&index=5&ab_channel=DoctorWho"

friends1 = "https://www.youtube.com/watch?v=ggZkZK-9Pm4&ab_channel=TBS"
friends2 = "https://www.youtube.com/watch?v=xHcPhdZBngw&ab_channel=TBS"
friends3 = "https://www.youtube.com/watch?v=VVQB_M2f6xM&ab_channel=TBS"
friends4 = "https://www.youtube.com/watch?v=11XnzEaFThU&ab_channel=TBS"

drama1 = video_url(doctor1,"The Best of the Twelfth Doctor #C=1499","doctor1")
drama2 = video_url(doctor2,"Doctor's Regenerations #C=5755","doctor2")

drama3 = video_url(friends1,"Friends: Best Moments of Season 1 to Binge at Home #C=3743","friends1")
drama4 = video_url(friends2,"Friends: Top 20 Funniest Moments #C=4270","friends2")
drama5 = video_url(friends3,"Friends: Chandler's Most Sarcastic Moments #C=2108","friends3")
drama6 = video_url(friends4,"Friends: Joey’s Top 22 Worst Advice Moments #C=1552","friends4")


#Comedy Central Stand-Up
central_standup1 = "https://www.youtube.com/watch?v=xs_zLnXsZH4&ab_channel=ComedyCentralStand-Up"
central_standup2 = "https://www.youtube.com/watch?v=xlonY2l3V9c&ab_channel=ComedyCentralStand-Up"
central_standup3 = "https://www.youtube.com/watch?v=e8QZwnJZTgQ&ab_channel=ComedyCentralStand-Up"
central_standup4 = "https://www.youtube.com/watch?v=3Sbw0lZ9LmY&ab_channel=ComedyCentralStand-Up"
central_standup5 = "https://www.youtube.com/watch?v=v3bfbIg1U5s&ab_channel=ComedyCentralStand-Up"

comedy1 = video_url(central_standup1,"Donald Glover - Advice from Tracy Morgan #C=2379","central_standup1")
comedy2 = video_url(central_standup2,"Hannibal Buress - Jaywalking Is a Fantasy Crime #C=2571","central_standup2")
comedy3 = video_url(central_standup3,"We Need a Dress Code at the Airport - Sebastian Maniscalco #C=4530","central_standup3")
comedy4 = video_url(central_standup4,"How Do 90% of Americans Have Jobs? - Daniel Tosh #C=7892","central_standup4")
comedy5 = video_url(central_standup5,"Josh Johnson Had to Prove He Was Black to a Blind Man #C=7049","central_standup5")

######################################################2차분석 대상#####################################################
#Wimbledon 2019 - Highlights and Match Clips
wimble1 = "https://www.youtube.com/watch?v=mnLdAeSXZv0&list=PLwx9gNibGUz6SzJb1zHdstIDrBBy1ZB0b&index=7&ab_channel=Wimbledon"
wimble2 = "https://www.youtube.com/watch?v=TUikJi0Qhhw&list=PLwx9gNibGUz6SzJb1zHdstIDrBBy1ZB0b&index=2&ab_channel=Wimbledon"
wimble3 = "https://www.youtube.com/watch?v=194cLdYnVF8&list=PLwx9gNibGUz6SzJb1zHdstIDrBBy1ZB0b&index=21&ab_channel=Wimbledon"
wimble4 = "https://www.youtube.com/watch?v=VRzVd1OZoaQ&list=PLwx9gNibGUz6SzJb1zHdstIDrBBy1ZB0b&index=8&ab_channel=Wimbledon"
wimble5 = "https://www.youtube.com/watch?v=J8__TwOgTY0&list=PLwx9gNibGUz6SzJb1zHdstIDrBBy1ZB0b&index=41&ab_channel=Wimbledon"

tennis1 = video_url(wimble1,"Novak Djokovic vs Roger Federer Wimbledon 2019 final highlights #C 6576 11:09","wimble1")
tennis2 = video_url(wimble2,"Novak Djokovic vs Roger Federer | Wimbledon 2019 | Full Match #C 5037 4:58:38","wimble2")
tennis3 = video_url(wimble3,"Novak Djokovic is the 2019 Wimbledon gentlemen's singles champion #C 1811 1:10","wimble3")
tennis4 = video_url(wimble4,"Simona Halep vs Serena Williams Wimbledon 2019 final highlights #C 1932 L: 5:35","wimble4")
tennis5 = video_url(wimble5,"Roger Federer vs Rafael Nadal Wimbledon 2019 semi-final highlights #C 3544 8:24","wimble5")


#2019 Game Recaps
mlb1 = "https://www.youtube.com/watch?v=hjO1-YY8nbA&list=PLL-lmlkrmJamiSMOFET46BizlvPmI-95I&index=5&ab_channel=MLB"
mlb2 = "https://www.youtube.com/watch?v=77jKOQVIH3Y&list=PLL-lmlkrmJamiSMOFET46BizlvPmI-95I&index=7&ab_channel=MLB"
mlb3 = "https://www.youtube.com/watch?v=cTibRn5TLMo&list=PLL-lmlkrmJamiSMOFET46BizlvPmI-95I&index=18&ab_channel=MLB"
mlb4 = "https://www.youtube.com/watch?v=K1JpV6ONsXw&list=PLL-lmlkrmJamiSMOFET46BizlvPmI-95I&index=1&ab_channel=MLB"
mlb5 = "https://www.youtube.com/watch?v=6RmSsVZf15I&list=PLL-lmlkrmJamiSMOFET46BizlvPmI-95I&index=6&ab_channel=MLB"

baseball1 = video_url(mlb1,"Nationals ride 6-run 7th to World Series Game 2 win | Nationals-Astros MLB Highlights #C 2156 9:51","mlb1")
baseball2 = video_url(mlb2,"Jose Altuve's walk-off HR sends Astros to World Series in Game 6! | Yankees-Astros MLB Highlights #C 3367 6:53","mlb2")
baseball3 = video_url(mlb3,"Howie Kendrick's grand slam lifts Nationals to NLCS over Dodgers | Nationals-Dodgers MLB Highlights #C 3459 7:53","mlb3")
baseball4 = video_url(mlb4,"Nationals win 1st World Series with Game 7 comeback win! | Astros-Nationals MLB Highlights #C 4148 11:19","mlb4")
baseball5 = video_url(mlb5,"Juan Soto homers, drives in 3 in Nats' World Series Game 1 win | Nationals-Astros MLB Highlights #C 1542 9:38","mlb5")


#NBA's Nightly Full Game Recaps 2018-19

nba1 = "https://www.youtube.com/watch?v=-LOluO9wJPc&list=PLlVlyGVtvuVkPjVoVoDG0sxbF0PYVvuTS&ab_channel=NBA"
nba2 = "https://www.youtube.com/watch?v=WT9lw1Stru0&list=PLlVlyGVtvuVkPjVoVoDG0sxbF0PYVvuTS&index=2&ab_channel=NBA"
nba3 = "https://www.youtube.com/watch?v=yOAyeJbjmS4&list=PLlVlyGVtvuVkPjVoVoDG0sxbF0PYVvuTS&index=3&ab_channel=NBA"
nba4 = "https://www.youtube.com/watch?v=MfgY7qxEISA&list=PLlVlyGVtvuVkPjVoVoDG0sxbF0PYVvuTS&index=5&ab_channel=NBA"
nba5 = "https://www.youtube.com/watch?v=16sOSdLoiOo&list=PLlVlyGVtvuVkPjVoVoDG0sxbF0PYVvuTS&index=6&ab_channel=NBA"

basketball1 = video_url(nba1,"RAPTORS vs WARRIORS | Toronto Wins First NBA Championship! | NBA Finals Game 6 #C 4237 9:33","nba1")
basketball2 = video_url(nba2,"WARRIORS vs RAPTORS | Unbelievable Finish at Scotiabank Arena | NBA Finals Game 5 #C 3499 9:39","nba2")
basketball3 = video_url(nba3,"WARRIORS vs ROCKETS | Stephen Curry Drops 33 Points in the 2nd Half | Game 6 #C 2340 9:31","nba3")
basketball4 = video_url(nba4,"WARRIORS vs RAPTORS | Toronto Grabs Franchise First Finals Win! | NBA Finals Game 1 #C 1678 9:36","nba4")
basketball5 = video_url(nba5,"RAPTORS vs WARRIORS | Kawhi Leonard Drops 36 Points in Oracle | NBA Finals Game 4 #C 1772 9:34","nba5")


#Movie(Real)
#From Youtube Channel - Movieclips

clips1 = "https://www.youtube.com/watch?v=K1R4hHq8yr4&ab_channel=Movieclips"
clips2 = "https://www.youtube.com/watch?v=jM7Eou4bV-Q&ab_channel=Movieclips"
clips3 = "https://www.youtube.com/watch?v=gAWrAQp7pWQ&ab_channel=Movieclips "
clips4 = "https://www.youtube.com/watch?v=2bpkd6hwH6U&ab_channel=Movieclips"
clips5 = "https://www.youtube.com/watch?v=yRhRZB-nqOU&ab_channel=Movieclips"

real_movie1 = video_url(clips1, "Indiana Jones 4 (9/10) Movie CLIP - Giant Ants (2008) HD #C 14784 2:42", "clips1")
real_movie2 = video_url(clips2, "Spider-Man Movie (2002) - Peter vs. Flash Scene (1/10) | Movieclips #C 7657 2:58", "clips2")
real_movie3 = video_url(clips3, "The Scorpion King (2/9) Movie CLIP - Fire Ants (2002) HD #C 6614 3:06", "clips3")
real_movie4 = video_url(clips4, "Now You See Me (2/11) Movie CLIP - The Piranha Tank (2013) HD #C 14566 2:23", "clips4")
real_movie5 = video_url(clips5, "Spider-Man 2 - Stopping the Train Scene (7/10) | Movieclips #C 20184 4:22", "clips5")

'''
    movies = [pixar2, pixar3]
    docus = [docu3, docu4, docu5]
    sports = [sport2,sport3,sport4,sport5]
    dramas = [drama2,drama3,drama4,drama5,drama6]
    comedies = [comedy2,comedy3,comedy4,comedy5]
'''

if __name__=="__main__":

    tennis_list = [tennis1, tennis2, tennis3, tennis4, tennis5]
    baseball_list = [baseball1, baseball2, baseball3, baseball4 ,baseball5]
    basketball_list = [basketball1,basketball2, basketball3, basketball4, basketball5]
    real_movie_list = [real_movie1, real_movie2, real_movie3, real_movie4, real_movie5]

    video_lists = [real_movie_list, tennis_list, basketball_list, baseball_list]
    
    for j in range(3):
        for target_list in video_lists:
            for video in target_list:
                
                print("anaylzing %s"%video.filename)
                output_file = open('%s-%d.txt'%(video.filename,j),'w',buffering=1)
                output_file.write('video info: '+video.info+'\n')
                output_file.write('url: '+video.url+'\n')

                html_source = crawl_youtube_page_html_source(video.url)
                if not html_source:
                    print("Skipping to next target video")
                    output_file.write("ERRRORROROROOROROROROOOR!!!!!!\n")
                    output_file.close()
                    continue

                timestamps_stats = get_timestamps(output_file,html_source)
                print_statistics(output_file,timestamps_stats)

                print("%s %dth analysis complete"%(video.filename,j))
                output_file.close()
                

