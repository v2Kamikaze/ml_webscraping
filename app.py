import scraper_mangas_links
from manga_model import MangaModel
from pprint import pprint

mangas_links = scraper_mangas_links.get_mangas_links_in_range(1, 5)
pprint(mangas_links)

manga: MangaModel = MangaModel()