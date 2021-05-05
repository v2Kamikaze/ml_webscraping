import time
from typing import Dict, List
from bs4 import BeautifulSoup
from requests import get
from urllib.parse import urljoin

# a url base para as páginas com as listas de mangás do site.
_BASE_URL: str = "https://mangalivre.net/series/index/nome/todos?page="

# o número máximo de páginas até o momento.
# ex: "https://mangalivre.net/series/index/nome/todos?page=401"
_CURRENT_MAX_NUMBER_PAGE: int = 401

# user-agent para não ser bloqueado pelo servidor (STATUS - 403).
_HEADERS: Dict[str, str] = {
    "User-Agent": "Mozilla/5.0",
}


def _set_range_pages(start: int, end: int) -> List[str]:
    """Cria uma lista de urls do intervalo inicial até o final
    a partir de _BASE_URL. Retorna uma lista vazia caso o
    intervalo não seja válido.

    :param start: o intervalo inicial de páginas. Deve ser maior que 0.

    :param end: o intervalo final de páginas. Deve ser maior que 0.

    :return:
        Uma lista contendo as urls no intervalo especificado.
    """
    if (start <= 0 or end <= 0) and start < end:
        return []
    return [_BASE_URL + str(i) for i in range(start, end+1)]


def _get_mangas_links(page_url: str) -> List[str]:
    """Faz uma requisição e busca na página as urls dos mangás
    contidos nela.

    :param page_url: a url da página onde estão presentes os mangás.

    :return:
        Uma lista contém todas as urls dos mangás da página.
    """

    res = get(page_url, headers=_HEADERS)
    if res.status_code == 200:
        soup = BeautifulSoup(res.text, "html.parser")
        mangas_links = soup.find_all("a", {"class": "link-block"})
        return [urljoin(_BASE_URL, link.get("href")) for link in mangas_links]
    return []


def get_mangas_links_in_range(
        start: int,
        end: int,
        sleep_time: int = 0) -> List[str]:
    """Busca as urls dos mangás no intervalo de páginas passado.

    :param start: o intervalo inicial de páginas. Deve ser maior que 0.

    :param end: o intervalo final de páginas. Deve ser maior que 0.

    :param sleep_time: o tempo em segundos que deverá se passar entre cada
    requisição. Por padrão é 0.

    :return:
        Uma lista que contém as urls dos mangás contidos em cada página.
    """
    all_mangas_in_page_range: List[str] = []
    pages_urls = _set_range_pages(start, end)
    for page_url in pages_urls:
        all_mangas_in_page_range += _get_mangas_links(page_url)
        time.sleep(sleep_time)
    return all_mangas_in_page_range
