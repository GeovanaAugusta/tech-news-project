from time import sleep
import requests
from parsel import Selector
from tech_news.database import create_news


def fetch(url):
    try:

        sleep(1)

        response = requests.get(url,
                                headers={"user-agent": "Fake user-agent",
                                         "Accept": "text/html"}, timeout=3)

        get_status_code = response.status_code

        if get_status_code == 200:
            return response.text
        else:
            return None

    except requests.exceptions.Timeout:
        return None


def scrape_updates(html_content):
    selector = Selector(text=html_content)

    urls_news = selector.css(".entry-title a::attr(href)").getall()

    if len(urls_news) > 0:
        return urls_news
    else:
        return []


def scrape_next_page_link(html_content):
    selector = Selector(text=html_content)

    next_page_url = selector.css("a.next::attr(href)").get()

    if next_page_url is not None:
        return next_page_url
    else:
        return None


def scrape_news(html_content):
    selector = Selector(html_content)

    url = selector.css("link[rel='canonical']::attr(href)").get()

    title = selector.css("h1.entry-title::text").get()
    timestamp = selector.css("li.meta-date::text").get()
    writer = selector.css("span.author a::text").get()
    comments_count = selector.css("h1.title-block::text").re_first("/d")

    s = (selector.xpath("string(//div[contains(@class,'entry-content')]/p)")
         .get())
    print(s)
    tags = selector.css("section.post-tags a::text").getall()
    category = selector.css("span.label::text").get()

    if title is None:
        return None
    else:
        news = {
                'url': url,
                'title': title.rstrip(),
                'timestamp': timestamp,
                'writer': writer,
                'comments_count': comments_count or 0,
                'summary': s.rstrip(),
                'tags': tags or [],
                'category': category
            }

    return news


def get_tech_news(amount):
    URL_BASE = "https://blog.betrybe.com/"

    response_text = fetch(URL_BASE)
    news = []

    while len(news) < amount:

        urls_news = scrape_updates(response_text)

        for url in urls_news:

            news.append(scrape_news(fetch(url)))

            # Interrompe o fluxo de next ou quebra tudo
            if len(news) == amount:
                break

        next_page_url = scrape_next_page_link(response_text)

        response_text = fetch(next_page_url)

    create_news(news)

    return news
