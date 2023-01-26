from tech_news.database import search_news
from datetime import datetime


def search_by_title(title):

    news_by_title = []

    news = search_news({
        "title": {

            "$regex": title,
            "$options": "i"
        }
    })

    news_by_title = [(new["title"], new["url"]) for new in news]

    if len(news_by_title) > 0:

        return news_by_title

    else:
        return []


def search_by_date(date):

    news_by_date = []

    try:
        previous_date = datetime.strptime(date, "%Y-%m-%d")

        final_date = datetime.strftime(previous_date, "%d/%m/%Y")

        news = search_news({
            "timestamp": final_date,
            }
        )

        news_by_date = [(new["title"], new["url"]) for new in news]

        if len(news_by_date) > 0:
            return news_by_date
        else:
            return []

    except ValueError:
        raise ValueError("Data inválida")


def search_by_tag(tag):
    news_by_tag = []

    news = search_news({
        "tags": {

            "$regex": tag,

            "$options": "i"
        }
    })

    news_by_tag = [(new["title"], new["url"]) for new in news]

    if len(news_by_tag) > 0:

        return news_by_tag

    else:
        return []


def search_by_category(category):
    news_by_category = []

    news = search_news({
        "category": {

            "$regex": category,

            "$options": "i"
        }
    })

    news_by_category = [(new["title"], new["url"]) for new in news]

    if len(news_by_category) > 0:

        return news_by_category

    else:
        return []
