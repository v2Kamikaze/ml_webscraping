"""from scraper_mangas_info import ScraperMangasInfo
from scraper_mangas_chapters import ScraperChapters

test_url = "https://mangalivre.net/manga/dorohedoro/728"
scraper_info = ScraperMangasInfo(headless_mode=True)
manga = scraper_info.get_manga_info(test_url)
scraper_info.close_browser()
file_name = "-".join(manga.title.lower().split(" ")) + ".json"
with open(file_name, "w") as file:
    scraper_chapter = ScraperChapters(timeout=60)
    scraper_chapter.get_chapter_pages(manga)
    scraper_chapter.close_browser()
    file.write(manga.to_json())
"""
from json_database import JsonDB
from manga_model import MangaModel

list_titles = ["kimetsu no Yaiba", "dorohedoro", "one piece"]

JsonDB.create_db_dir()
JsonDB.save_manga(MangaModel(title="kimetsu no Yaiba", status="completo"))
JsonDB.save_manga(MangaModel(title="dorohedoro", status="completo"))
JsonDB.save_manga(MangaModel(title="one piece", status="em lançamento"))
JsonDB.save_manga(MangaModel(title="jujust kaisen", status="em lançamento"))
JsonDB.save_manga(MangaModel(title="spy x family", status="em lançamento"))
JsonDB.save_list_titles(list_titles)
JsonDB.update_list_title(["kimetsu no Yaiba", "dorohedoro", "one piece", "toriko"])
