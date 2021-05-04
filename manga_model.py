from typing import List, Dict


class MangaModel:
    """Modelo que representa um mangá com todas as suas informações."""
    def __init__(self,
                 title: str = "",
                 alternative_titles: List[str] = None,
                 url: str = "",
                 status: str = "",
                 cover: str = "",
                 author: str = "",
                 categories: List[str] = None,
                 description: str = "",
                 chapters: Dict[str, List[str]] = None):
        """
        :param title: título do mangá.

        :param alternative_titles: títulos alternativos do mangá.

        :param url: url para acessar a página desse mangá.

        :param status: status do mangá, se está completo ou em andamento.

        :param cover: url da capa do mangá.

        :param author: autor do mangá.

        :param categories: categorias do mangá.

        :param description: sinopse do mangá.

        :param chapters: todos os capítulos do mangá até o momento.

        """

        self.title: str = title
        self.alternative_titles: List[str] = alternative_titles
        self.url: str = url
        self.cover: str = cover
        self.status: str = status
        self.author: str = author
        self.categories: List[str] = categories
        self.description: str = description
        self.chapters: Dict[str, List[str]] = chapters

    def __repr__(self):
        return f"""
        "title": {self.title},
        "alternative_titles": {self.alternative_titles},
        "url": {self.url},
        "covert": {self.cover},
        "status": {self.status},
        "author": {self.author},
        "categories": {self.categories},
        "description": {self.description},
        "chapters": {self.chapters}
        """
