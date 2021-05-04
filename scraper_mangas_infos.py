"""
scraper_mangas_infos é capaz de buscar as informações de um mangá específico.
A lista de capítulos é gerada por meio de javascript, então não é possível
obter a lista de capítulos por meio do requests e bs4.
"""
from typing import Dict, List
from requests import get
from bs4 import BeautifulSoup
from manga_model import MangaModel

# user-agent para não ser bloqueado pelo servidor (STATUS - 403).
_HEADERS: Dict[str, str] = {
    "User-Agent": "Mozilla/5.0",
}


def get_manga_info(manga_url: str) -> MangaModel:
    res = get(manga_url, headers=_HEADERS)
    url: str = manga_url
    title: str = _get_manga_title(res.text)
    cover: str = _get_manga_cover(res.text)
    status: str = _get_manga_status(res.text)
    author: str = _get_manga_author(res.text)
    description: str = _get_manga_description(res.text)
    categories: List[str] = _get_manga_categories(res.text)
    alternative_titles = _get_manga_alternative_titles(res.text)

    return MangaModel(
        title=title,
        author=author,
        url=url,
        cover=cover,
        status=status,
        description=description,
        categories=categories,
        alternative_titles=alternative_titles,
    )


def _get_manga_title(body: str) -> str:
    bs = BeautifulSoup(body, "html.parser")
    div_manga_info = bs.find("div", {"id": "series-data"})
    span_title = div_manga_info.find("span", {"class": "series-title"})
    manga_title = span_title.find("h1")
    return manga_title.text


def _get_manga_cover(body: str) -> str:
    bs = BeautifulSoup(body, "html.parser")
    div_manga_info = bs.find("div", {"id": "series-data"})
    manga_cover = div_manga_info.find("img", {"class": "cover"})
    return manga_cover.get("src")


def _get_manga_status(body: str) -> str:
    bs = BeautifulSoup(body, "html.parser")
    div_manga_info = bs.find("div", {"id": "series-data"})
    status = div_manga_info.find("i", {"class": "complete-series"})
    if status is None:
        return "Em lançamento"
    return status.text


def _get_manga_author(body: str) -> str:
    bs = BeautifulSoup(body, "html.parser")
    div_manga_info = bs.find("div", {"id": "series-data"})
    span_author = div_manga_info.find("span", {"class": "series-author"})
    author: str = ""
    for tag in span_author:
        if tag.name is None and tag.strip():
            author = tag.strip()
    return author


def _get_manga_categories(body: str) -> List[str]:
    bs = BeautifulSoup(body, "html.parser")
    div_manga_info = bs.find("div", {"id": "series-data"})
    div_categories = div_manga_info.find("div", {"class": "carousel"})
    categories = [
        c for c in div_categories.text.replace(" ", "").split("\n")
        if c.strip() != ""
    ]
    return categories


def _get_manga_description(body: str) -> str:
    bs = BeautifulSoup(body, "html.parser")
    div_manga_info = bs.find("div", {"id": "series-data"})
    span_description = div_manga_info.find("span", {"class": "series-desc"})
    description = span_description.find("span")
    return description.text


def _get_manga_alternative_titles(body: str) -> List[str]:
    bs = BeautifulSoup(body, "html.parser")
    div_manga_info = bs.find("div", {"id": "series-data"})
    ol_alternative_titles = div_manga_info.find("ol", {"class": "series-synom"})
    li_alternative_titles = ol_alternative_titles.find_all("li")
    alternative_titles = [t.text for t in li_alternative_titles]
    return alternative_titles
