from time import sleep
import requests
from parsel import Selector


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
    print(selector)


# Requisito 3
def scrape_next_page_link(html_content):
    """Seu código deve vir aqui"""


# Requisito 4
def scrape_news(html_content):
    """Seu código deve vir aqui"""


# Requisito 5
def get_tech_news(amount):
    """Seu código deve vir aqui"""

# SOURCE
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
