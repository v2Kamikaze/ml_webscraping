from typing import List
from scraper import ScraperChaptersMangaLivre
from pprint import pprint

urls: List[str] = [
    "https://mangalivre.net/ler/jujutsu-kaisen/online/296882/capitulo-147",
    "https://mangalivre.net/ler/jujutsu-kaisen/online/295135/capitulo-146",
    "https://mangalivre.net/ler/jujutsu-kaisen/online/293290/capitulo-145",
    "https://mangalivre.net/ler/jujutsu-kaisen/online/290310/capitulo-144",
]

scraper: ScraperChaptersMangaLivre = ScraperChaptersMangaLivre(
    timeout=30,
    headless_mode=False,
)

pprint(scraper.get_all_chapters(urls))

scraper.close_browser()
