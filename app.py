from scraper_mangas_info import ScraperMangasInfo
from scraper_mangas_chapters import ScraperChapters

with open("teste.json", "a") as file:
    test_url = "https://mangalivre.net/manga/spy-x-family/8103"
    scraper_info = ScraperMangasInfo()
    manga_test = scraper_info.get_manga_info(test_url)
    scraper_info.close_browser()
    scraper_chapter = ScraperChapters(timeout=30)
    scraper_chapter.get_chapter_pages(manga_test)
    scraper_chapter.close_browser()
    file.write(manga_test.to_json())
