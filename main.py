import json

import requests
from bs4 import BeautifulSoup


class HackerNewsScraper:
    def __init__(self, url="https://news.ycombinator.com/"):
        self.url = url
        self.albisteak = []

    def lortu_albisteak(self):
        try:
            res = requests.get(self.url, timeout=10)
            res.raise_for_status()
        except requests.RequestException as e:
            print(f"Errorea URL-a kargatzen: {e}")
            return []

        soup = BeautifulSoup(res.text, "html.parser")

        self.albisteak = []

        for elem in soup.find_all("span", class_="titleline"):
            a_tag = elem.find("a")
            if a_tag:
                titulua = a_tag.get_text()
                self.albisteak.append(titulua)

        return self.albisteak

    def gorde_json(self, fitxategi_izena: str = "hackernews.json"):
        if not self.albisteak:
            print("Ez da albisterik aurkitu gordetzeko.")
            return

        try:
            with open(fitxategi_izena, "w", encoding="utf-8") as f:
                json.dump(self.albisteak, f, ensure_ascii=False, indent=4)
            print(f"Albisteen tituluak gordeta '{fitxategi_izena}' fitxategian.")
        except OSError as e:
            print(f"Errorea fitxategian idaztean: {e}")


class PythonOrgScraper:
    def __init__(
        self, url: str = "https://www.python.org", albisteak: list | None = None
    ):
        self.url = url
        self.albisteak = albisteak

    def lortu_albisteak(self):
        try:
            res = requests.get(self.url, timeout=10)
            res.raise_for_status()
        except requests.RequestException as e:
            print(f"Errorea: {e}")
            return []

        soup = BeautifulSoup(res.text, "html.parser")

        self.albisteak = []

        news_widget = soup.find("div", class_="blog-widget")

        if news_widget:
            for al in news_widget.find_all("li"):
                a_tag = al.find("a")
                if a_tag:
                    titulua = a_tag.get_text(strip=True)
                    self.albisteak.append(titulua)

        return self.albisteak

    def gorde_json(self, fitxategi_izena: str = "pythonorg.json"):
        if not self.albisteak:
            print("Ez da albisterik aurkitu gordetzeko.")
            return

        try:
            with open(fitxategi_izena, "w", encoding="utf-8") as f:
                json.dump(self.albisteak, f, ensure_ascii=False, indent=4)
            print(f"Albisteen tituluak gordeta '{fitxategi_izena}' fitxategian.")
        except OSError as e:
            print(f"Errorea fitxategian idaztean: {e}")


class AlbisteKudeatzailea:
    def __init__(self, scraper_zerrenda: list | None = None):
        if scraper_zerrenda is None:
            self.scraperrak = []
        else:
            self.scraperrak = scraper_zerrenda

    def gehitu_scraper(self, scraper_objetua):
        self.scraperrak.append(scraper_objetua)

    def exekutatu_guztiak(self):
        for scraper in self.scraperrak:
            tituluak = scraper.lortu_albisteak()
            print(f"{len(tituluak)} albiste lortu dira")
            scraper.gorde_json()


if __name__ == "__main__":
    scraper1 = HackerNewsScraper()
    scraper2 = PythonOrgScraper()

    kudeatzailea = AlbisteKudeatzailea()
    kudeatzailea.gehitu_scraper(scraper1)
    kudeatzailea.gehitu_scraper(scraper2)

    kudeatzailea.exekutatu_guztiak()
