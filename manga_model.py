from typing import List, Dict, Any
from json import dumps


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
                 chapters: List[Dict[str, Any]] = None):
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
        self.chapters: List[Dict[str, Any]] = chapters

    def to_json(self) -> str:
        data: Dict[str, Any] = {
            "title": self.title,
            "url": self.url,
            "author": self.author,
            "alternative_titles": self.alternative_titles,
            "cover": self.cover,
            "status": self.status,
            "categories": self.categories,
            "description": self.description,
            "chapters": self.chapters,
        }
        return dumps(data, indent=4, ensure_ascii=False)

    @classmethod
    def from_json(cls, json_content: Dict[str, Any]) -> "MangaModel":
        return MangaModel(
            title=json_content["title"],
            url=json_content["url"],
            author=json_content["author"],
            alternative_titles=json_content["alternative_titles"],
            cover=json_content["cover"],
            status=json_content["status"],
            categories=json_content["categories"],
            description=json_content["description"],
            chapters=json_content["chapters"],
        )
