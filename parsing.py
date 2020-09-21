import urllib.request

from bs4 import BeautifulSoup

def parse(date):
    list_total = []  # 해당날짜 전체 기사의 url list
    article = []

    totalPageIdx = 1000  # pageIdx 탐색 개수
    # 해당 날짜의 전체 기사 링크들 저장
    for idx in range(1, totalPageIdx):
        url = "https://news.sbs.co.kr/news/newsflash.do?pageDate=" + \
            date+"&pageIdx="+str(idx)
        sourcecode = urllib.request.urlopen(
            url).read()
        soup = BeautifulSoup(sourcecode, "html.parser", from_encoding='ANSI')
        list_temp = []
        for href in soup.find("div", class_="w_news_list").find_all("li"):
            list_temp.append("https://news.sbs.co.kr"+href.find("a")["href"])

        # 노드가 더이상 없으면 종료
        if(len(list_temp) == 0):
            break
        for i in list_temp:
            list_total.append(i)

    # 기사 1개씩 탐색하며 list 에 추가
    for url in list_total:
        sourcecode = urllib.request.urlopen(
            url).read()
        soup = BeautifulSoup(sourcecode, "html.parser", from_encoding='ANSI')
        article.append({
            "title": soup.find(id="vmNewsTitle").get_text().replace('\n', ''),
            "body": soup.find("div", class_="text_area").get_text().replace('\n', ''),
            "date": soup.find("span", class_="date").get_text().replace('\n', '')[2:12],
            "link": url
        })
        print(url)
    return article

from datetime import datetime, timedelta
import json
print(json.dumps(["한글"], ensure_ascii=False))
print("한글")
if __name__ == "__main__":
    d = datetime.strptime("20190508", "%Y%m%d").date()
    for i in range(3650):
        tmp = d - timedelta(days=i)
        name = tmp.strftime("%Y%m%d")
        print(tmp.strftime("%Y%m%d"))
        tmp = parse(name)
        with open('tmp/' + name + '.json', 'w', encoding="utf-8") as f:
            f.write(json.dumps(tmp, ensure_ascii=False))

