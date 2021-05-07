import time

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.webelement import FirefoxWebElement
from selenium.webdriver.firefox import options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from typing import List, Tuple
from manga_model import MangaModel


class ScraperChapters:
    """
        ScraperChapters é uma classe que contém
        funcionalidades para remover informações de um ou
        muitos capítulos do site "https://mangalivre.net".
    """

    # diferença de tempo entre os cliquer na página.
    _CLICK_TIME = 0.5

    # tempo para se esperar entre uma request e outra se houver erro.
    _REQUEST_ERROR_TIME = 1

    # _URL_BASE_READER é a url base para para o leitor dos capítulos.
    # Se a url de um capítulo não contém _URL_BASE_READER, então não
    # pertence ao site "https://mangalivre.net".
    _URL_BASE_READER = "https://mangalivre.net/ler/"

    # seletor css para o elemento que contém o número total de páginas
    # do capítulo.
    CSS_SELECTOR_NUMBER_OF_PAGES: str = """
        #reader-wrapper > div:nth-child(10) >
        div.page-navigation-wrapper > div >
        div.page-navigation > span > em:nth-child(2)
    """

    # seletor css para o elemento onde as páginas do capítulo
    # são geradas com o javascript.
    CSS_SELECTOR_CHAPTER_PAGES: str = """
        #reader-wrapper > div.reader-content.fit.horizontal >
        div.manga-page > div > img
    """

    # seletor css para o elemento que contém o botão para
    # príxma página.
    CSS_SELECTOR_BUTTON_NEXT_PAGE: str = """
        #reader-wrapper > div:nth-child(10) >
        div.page-navigation-wrapper > div > div.page-next
    """

    CSS_SELECTOR_NUMBER_OF_CHAPTER: str = """
        #reader-wrapper > div.reader-navigation.clear-fix >
        div.chapter-selection-container > div.chapter-selection >
        span.current-chapter > em
    """

    CSS_SELECTOR_CHECK_BUTTON_18: str = """
        #reader-wrapper > div.reader-content.fit.horizontal >
        div.adult-warning-wrapper > div > div > a
    """

    CSS_BOX_CHECK_18: str = """
        #reader-wrapper > div.reader-content.fit.horizontal >
        div.adult-warning-wrapper
    """

    def __init__(self, timeout: int = 0, headless_mode: bool = False) -> None:
        """
        Classe responsável por retirar informações dos capítulos dos mangás
        contidos em "https://mangalivre.net" onde as páginas são
        geradas por meio de javascript.


        :param timeout: tempo em segundos que o navegador irá
        esperar para aparecerem as informações dos capítulos.

        :param headless_mode: define se o navegador será ou
        não renderizado. Por padrão, o navegador será renderizado.

        :return:
            None
        """
        self._options: options.Options = options.Options()
        self._options.headless = headless_mode
        self._browser: WebDriver = webdriver.Firefox(options=self._options)
        self._web_driver_wait = WebDriverWait(
            driver=self._browser,
            timeout=timeout,
        )

    def go_to_the_chapter(self, url: str) -> None:
        """
        Requisita ao navegador a página do capítulo da url passada.

        :param url: a url do capítulo de um mangá
        do site "https://mangalivre.net".

        :return:
            None
        """

        if self._URL_BASE_READER not in url:
            print(f"Url inválida! {self._browser.current_url}")
        try:
            self._browser.get(url)
        except TimeoutException:
            time.sleep(self._REQUEST_ERROR_TIME)
            self._browser.get(url)

    def _is_18(self) -> bool:
        """
        Retorna se um mangá é +18 ou não.

        :return:
            retorna True se for +18 e False se não.
        """

        button_locator: Tuple = (
            By.CSS_SELECTOR, self.CSS_BOX_CHECK_18
        )

        try:
            content = self._web_driver_wait.until(
                ec.visibility_of_element_located(button_locator)
            )
            # caso tenha conteúdo na caixa, o mangá é.
            return len(content.text.split()) != 0
        except TimeoutException:
            return False

    def _click_button_18(self):
        """
        Clica no botão para acessar o conteúdo +18.

        :return:
            None
        """
        button_locator: Tuple = (
            By.CSS_SELECTOR,
            self.CSS_SELECTOR_CHECK_BUTTON_18
        )
        try:
            button_18 = self._web_driver_wait.until(
                ec.element_to_be_clickable(button_locator)
            )
            button_18.click()
            time.sleep(self._CLICK_TIME)
        except TimeoutException:
            return

    def get_number_of_pages(self) -> int:
        """
        Retorna o número de páginas do capítulo atual no navegador.

        :return:
            o número de páginas do capítulo.
        """

        num_pages: int
        # locator_num_pages é o localizador da tag em onde está presente
        # o número de páginas do capítulo.
        locator_num_pages: Tuple = (
            By.CSS_SELECTOR, self.CSS_SELECTOR_NUMBER_OF_PAGES
        )

        try:
            # esperando que o elemento que contém o número
            # de páginas do capítulo fique visível.
            element_num_pages: FirefoxWebElement = self._web_driver_wait.until(
                ec.visibility_of_element_located(locator_num_pages)
            )
            num_pages = int(element_num_pages.text)
        except TimeoutException:
            print(
                f"""
                Erro ao buscar o número de páginas! {self._browser.current_url}
                """
            )
            return 0
        return num_pages

    def get_number_of_chapter(self) -> str:
        """Retorna o número do capítulo atual do que está no browser.

        :return:
            o número do capítulo.
        """

        number_of_chapter: str
        number_of_chapter_element: FirefoxWebElement
        # number_of_chapter_locator é o localizador da tag em onde
        # está presente o número do capítulo.
        number_of_chapter_locator: Tuple = (
            By.CSS_SELECTOR,
            self.CSS_SELECTOR_NUMBER_OF_CHAPTER
        )

        try:
            # esperando que o elemento que contém o número
            # do capítulo fique visível.
            number_of_chapter_element = self._web_driver_wait.until(
                ec.visibility_of_element_located(
                    number_of_chapter_locator
                )
            )
            number_of_chapter = number_of_chapter_element.text
        except TimeoutException:
            print(f"""
                Erro ao buscar número do capítulo: {self._browser.current_url}!
            """)
            return ""

        return number_of_chapter

    def get_pages(self, number_of_pages: int = 0) -> List[str]:
        """
        Retorna uma lista com os links das imagens do capítulo.

        :param number_of_pages: número de páginas do capítulo atual.
        O número de páginas - 1 é o número de cliques necessários
        para obter todas as páginas do capítulo, já que o capítulo
        começa pela página 1.

        :return:
            uma lista com todas as páginas do capítulo.
        """
        list_pages: List[str] = []
        # page_element é o elemento em que as páginas são renderizadas.
        page_element: FirefoxWebElement
        # button_element é o elemento com o botão para passar as páginas.
        button_element: FirefoxWebElement

        for _ in range(number_of_pages - 1):
            # obtendo a tag img onde está a página do campítulo.
            page_element = self._browser.find_element_by_css_selector(
                self.CSS_SELECTOR_CHAPTER_PAGES
            )
            # obtendo o link da página do capítulo.
            page_link: str = page_element.get_attribute("src")
            if page_link:
                list_pages.append(page_link)

            # obtendo o botão resposável por passar as páginas.
            button_element = self._browser.find_element_by_css_selector(
                self.CSS_SELECTOR_BUTTON_NEXT_PAGE
            )
            # clicando no botão e carregando a próxima página do capítulo.
            button_element.click()
            time.sleep(self._CLICK_TIME)

        return list_pages

    def get_chapter_pages(self, manga: MangaModel):
        """Insere as páginas e o número de páginas no seu capítulo
        específico. O mangá tem que estar inicializado por get_manga_info().

        :param manga: um modelo de mangá já inicializado.

        :return:
            None
        """
        for chapter in manga.chapters:
            chapter_url = chapter["url"]
            self.go_to_the_chapter(chapter_url)
            # verificando se o mangá é +18.
            # caso seja, irá clicar na caixa de checagem.
            if self._is_18():
                self._click_button_18()

            number_of_pages: int = self.get_number_of_pages()
            chapter_pages: List[str] = self.get_pages(number_of_pages)
            chapter["pages"] = chapter_pages
            chapter["number_of_pages"] = number_of_pages

    def close_browser(self) -> None:
        """
        Finaliza o navegador e fecha todas as janelas associadas à ele.

        :return:
            None
        """
        self._browser.quit()
