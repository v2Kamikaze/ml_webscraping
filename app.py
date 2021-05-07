from scraper_mangas_info import ScraperMangasInfo
from scraper_mangas_chapters import ScraperChapters
from scraper_mangas_links import get_mangas_links_in_range
from json_database import JsonDB


JsonDB.create_db_dir()
mangas_links = get_mangas_links_in_range(2, 2, sleep_time=1)
JsonDB.save_list_titles(mangas_links)


for manga_link in mangas_links:
    scraper_info = ScraperMangasInfo()
    manga = scraper_info.get_manga_info(manga_link)
    scraper_info.close_browser()
    JsonDB.save_manga(manga)
    scraper_chapters = ScraperChapters(timeout=30)
    scraper_chapters.get_chapter_pages(manga)
    JsonDB.save_manga(manga)
    scraper_chapters.close_browser()
