import time
from selenium import webdriver
from selenium.webdriver.firefox import options
from selenium.webdriver.firefox.webdriver import WebDriver
from typing import Dict, Any, List
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from manga_model import MangaModel


class ScraperMangasInfo:
    """
    ScraperMangasInfo é a classe que contém
    funcionalidades para remover informações de um mangá
    ou muitos mangás do site "https://mangalivre.net".
    """

    # id do footer da página.
    _ID_FOOTER: str = "social-media"

    def __init__(self, headless_mode: bool = False) -> None:
        """
        :param headless_mode: define se o navegador será renderizado
        ou não. Por padrão (headless_mode = False), o navegador será
        renderizado.

        :return:
            None
        """
        self._options: options.Options = options.Options()
        self._options.headless = headless_mode
        self._browser: WebDriver = webdriver.Firefox(options=self._options)

    def _wait_for_list_load(self):
        """Espera o carregamento total da lista de mangás.

            :return:
                None
        """
        last_page_height = self._browser.execute_script(
            "return document.body.scrollHeight"
        )
        # Dando scroll até que a lista seja completamente carregada,
        # se a nova posiçao do stroll for igual a última, então a tela já
        # foi totalmente carregada.
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
        """Requisita ao navegador a página do mangá da url passada.

        :param manga_url: url do mangá que deseja as informações serão
        retiradas.

        :return:
            None
        """
        self._browser.get(manga_url)
        self._wait_for_list_load()

    def get_manga_info(self, manga_url: str) -> MangaModel:
        """Obtém todas as informações do mangá passado e retorna
        um objeto com todas as informações retiradas nele.

        :param manga_url: url do mangá que deseja remover as informações.

        :return:
            MangaModel
        """
        self._go_to_the_manga(manga_url=manga_url)
        url: str = self._browser.current_url
        title: str = self._get_manga_title()
        cover: str = self._get_manga_cover()
        status: str = self._get_manga_status()
        author: str = self._get_manga_author()
        description: str = self._get_manga_description()
        categories: List[str] = self._get_manga_categories()
        alternative_titles = self._get_manga_alternative_titles()
        chapters: List[Dict[str, Any]] = self._get_manga_list_chapters()

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
        """
        Obtém o título do mangá.

        :return:
            uma string com o título do mangá.
        """
        bs = BeautifulSoup(self._browser.page_source, "html.parser")
        div_manga_info = bs.find("div", {"id": "series-data"})
        span_title = div_manga_info.find("span", {"class": "series-title"})
        manga_title = span_title.find("h1")
        return manga_title.text

    def _get_manga_cover(self) -> str:
        """
        Obtém a capa do mangá.

        :return:
            uma string contendo a url da capa do mangá.
        """
        try:
            bs = BeautifulSoup(self._browser.page_source, "html.parser")
            div_manga_info = bs.find("div", {"id": "series-data"})
            manga_cover = div_manga_info.find("img", {"class": "cover"})
        # se retornar None para a capa.
        except AttributeError:
            return ""
        return manga_cover.get("src")

    def _get_manga_status(self) -> str:
        """
        Obtém o status do mangá.

        :return:
            uma string contendo "completo" caso o mangá esteja finalizado,
            ou "em laçamento" caso o contrário.
        """
        try:
            bs = BeautifulSoup(self._browser.page_source, "html.parser")
            div_manga_info = bs.find("div", {"id": "series-data"})
            i_status = div_manga_info.find("i", {"class": "complete-series"})
            status = i_status.text.lower()
        # retornou None para o status.
        except AttributeError:
            return "em lançamento"

        return status

    def _get_manga_author(self) -> str:
        """
        Obtém o autor de mangá.

        :return:
            retorna uma string com o nome do autor do mangá.
        """
        try:
            bs = BeautifulSoup(self._browser.page_source, "html.parser")
            div_manga_info = bs.find("div", {"id": "series-data"})
            span_author = div_manga_info.find(
                "span", {"class": "series-author"}
            )
            author: str = ""
            for tag in span_author:
                if tag.name is None and tag.strip():
                    tag_author = tag.strip()
                    line_author = tag_author.split(" ")
                    line_author = [
                        name for name in line_author
                        if name != ""
                    ]
                    author = " ".join(line_author)
        # retornou None para o autor.
        except AttributeError:
            return ""

        return author

    def _get_manga_categories(self) -> List[str]:
        """
        Obtém as categorias do mangá.

        :return:
            uma lista de categorias das quais o mangá faz parte.
        """
        try:
            bs = BeautifulSoup(self._browser.page_source, "html.parser")
            div_manga_info = bs.find("div", {"id": "series-data"})
            div_categories = div_manga_info.find("div", {"class": "carousel"})
            # Não possui categorias
            if div_categories is None:
                return []

            categories = [
                c for c in div_categories.text.replace(" ", "").split("\n")
                if c.strip() != ""
            ]
        # retornou None para as categorias.
        except AttributeError:
            return []

        return categories

    def _get_manga_description(self) -> str:
        """
        Obtém a descrição do mangá.

        :return:
            uma string contendo a sinopse do mangá.
        """
        try:
            bs = BeautifulSoup(self._browser.page_source, "html.parser")
            div_manga_info = bs.find("div", {"id": "series-data"})
            span_description = div_manga_info.find(
                "span", {"class": "series-desc"}
            )
            description = span_description.find("span").text
        # retornou None para a descrição.
        except AttributeError:
            return ""

        return description

    def _get_manga_alternative_titles(self) -> List[str]:
        """
        Obtém os títulos alternativos do mangá.

        :return:
            uma lista com todos os títulos alternativos do mangá.
        """
        try:
            bs = BeautifulSoup(self._browser.page_source, "html.parser")
            div_manga_info = bs.find("div", {"id": "series-data"})
            ol_alternative_titles = div_manga_info.find(
                "ol", {"class": "series-synom"}
            )
            li_alternative_titles = ol_alternative_titles.find_all("li")
            alternative_titles = [t.text for t in li_alternative_titles]
        # retornou None para a lista de títulos alternativos.
        except AttributeError:
            return []
        return alternative_titles

    def _get_manga_list_chapters(self) -> List[Dict[str, Any]]:
        """
        Obtém a lista de capítulos do mangá. A lista é gerada por
        javascript.

        :return:
            um dicionário com cada chave representando um número de
            capítulo e contém a url desse capítulo.
        """
        all_chapters: List[Dict[str, Any]] = []
        res_body: str = self._browser.page_source
        try:
            bs = BeautifulSoup(res_body, "html.parser")
            div_list_chapters = bs.find("div", {"id": "chapter-list"})
            ul_chapters = div_list_chapters.find("ul", {"full-chapters-list"})
            lis_chapters = ul_chapters.find_all("li")

            for li_chapter in lis_chapters:
                current_chapter: Dict[str, Any] = {}
                chapter_number = li_chapter.find("span", {"class": "cap-text"})
                chapter_url = li_chapter.find(
                    "a",
                    {"class": "link-dark"}
                ).get("href")

                chapter_url = urljoin(
                    self._browser.current_url, chapter_url
                )
                current_chapter["pages"] = []
                current_chapter["number_of_pages"] = 0
                current_chapter["number_of_chapter"] = chapter_number.text
                current_chapter["url"] = chapter_url
                all_chapters.append(current_chapter)
        # retornou None para a lista de capítulos.
        except AttributeError:
            return []
        return all_chapters

    def close_browser(self):
        """
        Finaliza o navegador e fecha todas as janelas associadas à ele.

        :return:
            None
        """
        self._browser.quit()
