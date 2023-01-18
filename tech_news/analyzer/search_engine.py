# Requisito 6
from tech_news.database import search_news


def search_by_title(title):

    news_by_title = []

    news = search_news({
        "title": {
            # Deve buscar as notícias do banco de dados por título
            "$regex": title,
            # A busca deve ser case insensitive
            "$options": "i"
        }
    })
    # print("news", news)

    news_by_title = [(new["title"], new["url"]) for new in news]
    # print(news_by_title)

    if len(news_by_title) > 0:

        return news_by_title

    else:
        return []


# Requisito 7
def search_by_date(date):
    """Seu código deve vir aqui"""


# Requisito 8
def search_by_tag(tag):
    news_by_tag = []

    news = search_news({
        "tags": {
            # Deve buscar as notícias do banco de dados pela tag
            "$regex": tag,
            # A busca deve ser case insensitive
            "$options": "i"
        }
    })

    news_by_tag = [(new["title"], new["url"]) for new in news]
    # print(news_by_tag)

    if len(news_by_tag) > 0:

        return news_by_tag

    else:
        return []


# Requisito 9
def search_by_category(category):
    """Seu código deve vir aqui"""
    # news_by_category = []

    # news = search_news({
    #     "category": {
    #         # Deve buscar as notícias do banco de dados pela tag
    #         "$regex": category,
    #         # A busca deve ser case insensitive
    #         "$options": "i"
    #     }
    # })

# SOURCE
# Requisito 6
# Dia 02
# Buscas
# client = MongoClient()
# db = client.catalogue
# # busca um documento da coleção, sem filtros
# print(db.books.find_one())
# # busca utilizando filtros
# for book in db.books.find({"title": {"$regex": "t"}}):
#     print(book["title"])
# client.close()
# insensitive case
# https://stackoverflow.com/questions/8246019/case-insensitive-search-in-mongo
# https://www.mongodb.com/docs/manual/reference/operator/query/regex/
