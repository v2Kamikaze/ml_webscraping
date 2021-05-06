from scraper_mangas_info import ScraperMangasInfo
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
