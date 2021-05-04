import time
from selenium import webdriver
from selenium.webdriver.firefox import options
from selenium.webdriver.firefox.webdriver import WebDriver
from typing import Dict, Any, List
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from manga_model import MangaModel


class ScraperMangasInfoMangaLivre:

    _ID_FOOTER: str = "social-media"

    def __init__(self, headless_mode: bool = False) -> None:
        self._options: options.Options = options.Options()
        self._options.headless = headless_mode
        self._browser: WebDriver = webdriver.Firefox(options=self._options)

    def _wait_for_screen_scroll(self):
        last_page_height = self._browser.execute_script(
            "return document.body.scrollHeight"
        )
        while True:
            self._browser.execute_script(
                "window.scrollTo(0,document.documentElement.scrollHeight);"
            )
            time.sleep(0.5)
            new_page_height = self._browser.execute_script(
                "return document.body.scrollHeight"
            )
            if new_page_height == last_page_height:
                return
            last_page_height = new_page_height

    def _go_to_the_manga(self, manga_url: str):
        self._browser.get(manga_url)
        self._wait_for_screen_scroll()

    def _get_manga_list_chapters(self) -> Dict[str, Any]:
        all_chapters: Dict[str, str] = {}
        res_body: str = self._browser.page_source
        bs = BeautifulSoup(res_body, "html.parser")
        div_list_chapters = bs.find("div", {"id": "chapter-list"})
        ul_chapters = div_list_chapters.find("ul", {"full-chapters-list"})
        lis_chapters = ul_chapters.find_all("li")

        for li_chapter in lis_chapters:
            chapter_number = li_chapter.find("span", {"class": "cap-text"})
            chapter_url = li_chapter.find(
                "a",
                {"class": "link-dark"}
            ).get("href")

            all_chapters[chapter_number.text] = urljoin(
                self._browser.current_url, chapter_url
            )

        return all_chapters

    def get_manga_info(self, manga_url: str) -> MangaModel:
        self._go_to_the_manga(manga_url=manga_url)
        url: str = self._browser.current_url
        title: str = self._get_manga_title()
        cover: str = self._get_manga_cover()
        status: str = self._get_manga_status()
        author: str = self._get_manga_author()
        description: str = self._get_manga_description()
        categories: List[str] = self._get_manga_categories()
        alternative_titles = self._get_manga_alternative_titles()
        chapters: Dict[str, Any] = self._get_manga_list_chapters()

        return MangaModel(
            title=title,
            author=author,
            url=url,
            cover=cover,
            status=status,
            description=description,
            categories=categories,
            alternative_titles=alternative_titles,
            chapters=chapters
        )

    def _get_manga_title(self) -> str:
        bs = BeautifulSoup(self._browser.page_source, "html.parser")
        div_manga_info = bs.find("div", {"id": "series-data"})
        span_title = div_manga_info.find("span", {"class": "series-title"})
        manga_title = span_title.find("h1")
        return manga_title.text

    def _get_manga_cover(self) -> str:
        bs = BeautifulSoup(self._browser.page_source, "html.parser")
        div_manga_info = bs.find("div", {"id": "series-data"})
        manga_cover = div_manga_info.find("img", {"class": "cover"})
        return manga_cover.get("src")

    def _get_manga_status(self) -> str:
        bs = BeautifulSoup(self._browser.page_source, "html.parser")
        div_manga_info = bs.find("div", {"id": "series-data"})
        status = div_manga_info.find("i", {"class": "complete-series"})
        if status is None:
            return "Em lançamento"
        return status.text

    def _get_manga_author(self) -> str:
        bs = BeautifulSoup(self._browser.page_source, "html.parser")
        div_manga_info = bs.find("div", {"id": "series-data"})
        span_author = div_manga_info.find("span", {"class": "series-author"})
        author: str = ""
        for tag in span_author:
            if tag.name is None and tag.strip():
                author = tag.strip()
        return author

    def _get_manga_categories(self) -> List[str]:
        bs = BeautifulSoup(self._browser.page_source, "html.parser")
        div_manga_info = bs.find("div", {"id": "series-data"})
        div_categories = div_manga_info.find("div", {"class": "carousel"})
        categories = [
            c for c in div_categories.text.replace(" ", "").split("\n")
            if c.strip() != ""
        ]
        return categories

    def _get_manga_description(self) -> str:
        bs = BeautifulSoup(self._browser.page_source, "html.parser")
        div_manga_info = bs.find("div", {"id": "series-data"})
        span_description = div_manga_info.find(
            "span", {"class": "series-desc"}
        )
        description = span_description.find("span")
        return description.text

    def _get_manga_alternative_titles(self) -> List[str]:
        bs = BeautifulSoup(self._browser.page_source, "html.parser")
        div_manga_info = bs.find("div", {"id": "series-data"})
        ol_alternative_titles = div_manga_info.find(
            "ol", {"class": "series-synom"}
        )
        li_alternative_titles = ol_alternative_titles.find_all("li")
        alternative_titles = [t.text for t in li_alternative_titles]
        return alternative_titles

    def close_browser(self):
        self._browser.quit()
