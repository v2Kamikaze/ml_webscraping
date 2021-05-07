import os
from json import dumps, loads
from typing import List
from manga_model import MangaModel


class JsonDB:
    """
    JsonDB é um banco de dados simples, onde usa somente arquivos
    json para salvar os dados.
    """

    # path completo dos diretórios do banco de dados json.
    _FULL_DIR: str = "json_db/list_titles"
    # path do banco de dados em si, onde serão armazeados os
    # títulos.
    _DB_DIR: str = "json_db"

    @classmethod
    def create_db_dir(cls):
        """
        Cria os diretórios do banco de dados json se não existirem.

        :return:
            None
        """
        try:
            os.makedirs(cls._FULL_DIR)
        # o diretório já existe.
        except FileExistsError:
            return

    @classmethod
    def save_list_titles(cls, list_titles: List[str]):
        """
        Salva a lista de títulos no banco de dados.

        :param list_titles: uma lista contendo os títulos ou urls dos mangás.

        :return:
            None
        """
        file_dir = cls._FULL_DIR + "/list_titles.json"
        with open(file_dir, "w+", encoding="utf-8") as file:
            file.write(dumps(list_titles, ensure_ascii=False, indent=4))

    @classmethod
    def update_list_title(cls, new_list_titles: List[str]):
        """
        Atualiza a lista de títulos no banco de dados json.

        :param new_list_titles: a nova lista contendo os títulos
        atualizados.

        :return:
            None
        """
        file_dir = cls._FULL_DIR + "/list_titles.json"
        outdated_file = open(file_dir, "r", encoding="utf-8")
        outdated_list = loads(outdated_file.read())
        outdated_file.close()
        with open(file_dir, "w+", encoding="utf-8") as updated_file:
            for title in new_list_titles:
                if title not in outdated_list:
                    outdated_list.append(title)
            updated_file.write(dumps(outdated_list, ensure_ascii=False, indent=4))

    @classmethod
    def save_manga(cls, manga: MangaModel):
        """
        Salva um mangá no banco de dados json.

        :param manga: um modelo de mangá já inicializado.

        :return:
            None
        """
        name_file = "-".join(manga.title.lower().split(" ")) + ".json"
        with open(cls._DB_DIR + "/" + name_file, "w+", encoding="utf-8") as file:
            file.write(manga.to_json())
