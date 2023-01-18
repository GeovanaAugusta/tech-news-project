from time import sleep
import requests
from parsel import Selector
from tech_news.database import create_news


# Requisito 1
def fetch(url):
    try:
        # Garante que cada req seja feita com um intervalo de 1 s, antes da req
        sleep(1)
        # requisição para essa instância criada utilizando o método `get`
        response = requests.get(url,
                                headers={"user-agent": "Fake user-agent",
                                         "Accept": "text/html"}, timeout=3)
        # print(response)
        get_status_code = response.status_code

# use ==/!= to compare constant literals (str, bytes, int, float, tuple),
# quando tentei usar is
        if get_status_code == 200:
            return response.text
        else:
            return None

    except requests.exceptions.Timeout:
        return None


# Requisito 2
def scrape_updates(html_content):
    selector = Selector(text=html_content)

    urls_news = selector.css(".entry-title a::attr(href)").getall()

    if len(urls_news) > 0:
        return urls_news
    else:
        return []


# Requisito 3
def scrape_next_page_link(html_content):
    selector = Selector(text=html_content)

    next_page_url = selector.css("a.next::attr(href)").get()

    # print("next", next_page_url) retorna None quando encontra nada
    if next_page_url is not None:
        return next_page_url
    else:
        return None


# Requisito 4
def scrape_news(html_content):
    selector = Selector(html_content)
# [<Selector xpath="descendant-or-self::link[@rel = 'canonical']"
# data='<link rel="canonical" href="https://b...'>],
    url = selector.css("link[rel='canonical']::attr(href)").get()
    # print("url", url)
    title = selector.css("h1.entry-title::text").get()
    timestamp = selector.css("li.meta-date::text").get()
    writer = selector.css("span.author a::text").get()
    comments_count = selector.css("h1.title-block::text").re_first("/d")
    # .xpath('//tag mãe[contains(@class, "nome da classe")]/tag filha)
    # Sem transformar em string o texto do sumário vem dentro da tag <p>
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


# Requisito 5
def get_tech_news(amount):
    URL_BASE = "https://blog.betrybe.com/"
    # Tenho meu retorno do fetch para a url base e posteriores
    response_selector = fetch(URL_BASE)
    news = []

    while len(news) < amount:
        # A partir da lista de urls obtidas
        urls_news = scrape_updates(response_selector)

        for url in urls_news:

            # Faço fetch url a url -> array de objetos com infos sobre as news
            # 2 horas depois: como é item a item que vou adicionando
            # Precisa ser append e não extend
            news.append(scrape_news(fetch(url)))

            # Interrompe o fluxo de next ou quebra tudo
            if len(news) == amount:
                break

        # Aqui obtenho a próxima page, pela url dela pra fazer um novo fetch e
        # assim renderizar a nova pág
        next_page_url = scrape_next_page_link(response_selector)
        # print("next_page_url", next_page_url)

        response_selector = fetch(next_page_url)

    create_news(news)
    # print("news", news)

    return news

# SOURCE

# Requisito 1
# Dia 02 - Exercício 3
# response = requests.get(
#     "https://scrapethissite.com/pages/advanced/?gotcha=headers",
#     headers={"User-agent": "Mozilla", "Accept": "text/html"},
# )
# https://www.datacamp.com/tutorial/making-http-requests-in-python
# Estrutura base
#     try:

    # Busca pela tag 'a' com as classes específicas do link desejado
    #     return soup_page.find(
    #         "a",
    #         {"class": "tec--btn"},
    #     )["href"]
    # except TypeError:
    #     return None
# Pegar apenas o número do status retornado
# https://www.pluralsight.com/guides/web-scraping-with-request-python
# Except para quando extrapola o timeout
# https://stackoverflow.com/questions/28377421/why-do-i-receive-a-timeout-error-from-pythons-requests-module

# Requisito 2
# Dia 02
# response = requests.get("http://books.toscrape.com/")
# selector = Selector(text=response.text)
# print(selector)

# O título está no atributo title em um elemento âncora (<a>)
# Dentro de um h3 em elementos que possuem classe product_pod
# titles = selector.css(".product_pod h3 a::attr(title)").getall()
# Tamanho de um array
# https://www.digitalocean.com/community/tutorials/find-the-length-of-a-list-in-python

# Requisito 3
# Dia 02
# Descobre qual é a próxima página
    # next_page_url = selector.css(".next a::attr(href)").get()

# Requisito 4
# Remover caracter no final
# https://www.freecodecamp.org/news/python-strip-how-to-trim-a-string-or-line/#:~:text=of%20a%20string.-,Use%20the%20.,the%20end%20of%20a%20string.
# Pegar apenas número = re_first("[0-9]") ou "/d"
# https://parsel.readthedocs.io/en/latest/usage.html
# Pelo que entendi o url canônico é o + representativo em um grupo de páginas
# Evita problemas de conteúdo duplicado na otimização de mecanismos de pesquisa

# Requisito 5
# Dia 02
# Recurso por recurso
# https://www.freecodecamp.org/news/python-list-append-vs-python-list-extend/#:~:text=append()%20adds%20a%20single,the%20end%20of%20the%20list.
