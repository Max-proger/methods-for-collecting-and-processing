import requests
from lxml import html
from pymongo import MongoClient, errors

url = "https://lenta.ru/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"
}
response = requests.get(url, headers=headers)

dom = html.fromstring(response.text)
items = dom.xpath('//a[contains(@class, "_topnews")]')

client = MongoClient("127.0.0.1", 27017)
db = client["lenta_news_database"]
lenta_news = db.lenta_news


for item in items:
    news = {}
    source = "lenta.ru"
    title = item.xpath('.//*[contains(@class, "_title")]/text()')[
        0
    ]  # .//h3 | //a[contains(@class, "_topnews")]//span[@class="card-mini__title"]/text()
    link = url + item.get("href")
    date_publication = item.xpath(".//time/text()")[0]

    try:
        lenta_news.insert_one(
            {
                "_id": link,
                "title": title,
                "link": link,
                "date_publication": date_publication,
            }
        )
    except errors.DuplicateKeyError:
        continue
