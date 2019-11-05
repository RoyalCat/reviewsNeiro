import pandas as pd
from selenium import webdriver
import re

#proxy = webdriver.Proxy()
#proxy.http_proxy= '220.143.187.219:3128'
#proxy.socks_proxy = '220.143.187.219:3128'
#proxy.ssl_proxy = '220.143.187.219:3128'
#capabilities = webdriver.DesiredCapabilities.FIREFOX
#proxy.add_to_capabilities(capabilities)

browser = webdriver.Firefox()# desired_capabilities=capabilities)


def getFilmReviews(filmid):
    browser.get("https://www.kinopoisk.ru/film/" + str(filmid) + "/reviews/ord/date/status/all/perpage/200/")
    #raw = str(requests.get("https://www.kinopoisk.ru/film/" + str(filmid) + "/reviews/ord/date/status/all/perpage/200/").content)
    raw = str(browser.page_source)
    reviewsDic = {
        'filmName': [],
        'author': [],
        'date': [],
        'opinion': [],
        'text': []
        }
    filmNameRegex = r'(<a href="\/film\/\d{0,8}\/" class="\S{0,}" data-popup-info="disabled">)(.{0,40})(?=<\/a>)'
    try:
        filmName = re.findall(filmNameRegex, raw)[0][1]
    except:
        return reviewsDic
    while True:
        reviewBlockStart = raw.find('<div class="reviewItem userReview"')
        if reviewBlockStart == -1:
            break

        reviewBlockEnd = raw.find('<ul class="voter">', reviewBlockStart)
             
        reviewsDic['filmName'].append(filmName)

        opinionStartPos = raw.find('<div class="response ', reviewBlockStart, reviewBlockEnd)+21
        opinion = raw[opinionStartPos:opinionStartPos+4]
        if opinion == 'good':
            reviewsDic['opinion'].append(1)
        else:
            reviewsDic['opinion'].append(0)
        
        authorStartPos = raw.find('<p class="profile_name"><s></s><a href="/user/', reviewBlockStart, reviewBlockEnd)+46
        reviewsDic['author'].append(raw[authorStartPos:raw.find("/", authorStartPos)-1])

        textStartPos = raw.find('<span class="_reachbanner_" itemprop="reviewBody">', reviewBlockStart, reviewBlockEnd)+50
        text = raw[textStartPos:raw.find("</p>" , textStartPos)-1]
        text = re.sub(r'<.{1,}>', ' ', text)
        text = re.sub(r'[^\w]', ' ', text)
        reviewsDic['text'].append(text)
        
        dateStartPos = raw.find('<span class="date">', reviewBlockStart, reviewBlockEnd)+19
        reviewsDic['date'].append(raw[dateStartPos:raw.find('</span>', dateStartPos)])

        raw = raw[reviewBlockEnd:]
        
    return reviewsDic

def getFilmsId(url):
    browser.get(url)
    raw = str(browser.page_source)
    findidRegex = r'(?<=<a href="\/film\/)(\d{7})(?=\/")'
    ids = re.findall(findidRegex, raw)
    return ids


ids = list(dict.fromkeys(getFilmsId("https://www.kinopoisk.ru/popular/")))
allReviewisDic ={
        'filmName': list(),
        'author': list(),
        'date': list(),
        'opinion': list(),
        'text': list()
        }
for id in ids:
    filmReviews = getFilmReviews(id)
    #dic.append(getFilmReviews(id), ignore_index=True)
    for column in allReviewisDic.keys():
        allReviewisDic[column].extend(filmReviews[column])

browser.quit()
df = pd.DataFrame(allReviewisDic)
df.to_csv("reviewdf.csv")
print(df)