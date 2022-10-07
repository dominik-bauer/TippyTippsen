"""
Provides methods to scrape match data and rankings from sportschau.de
"""

import bs4
import requests
from exceptions import ScrapingError
from datetime import datetime


def scrape_matches() -> list[tuple[datetime, bool]]:
    """
    Returns a list of tuples. Each tuple contains starting time of a match
    and if that match is already finished. The list contains past, current
    or future  matches of the relevant "Spieltage" as listed on sportschau.de. The list
    contains the combined matches of 1., 2. and 3. Bundesliga
    """

    urls = [
        "https://www.sportschau.de/live-und-ergebnisse/fussball/deutschland-bundesliga",
        "https://www.sportschau.de/live-und-ergebnisse/fussball/deutschland-2-bundesliga",
        "https://www.sportschau.de/live-und-ergebnisse/fussball/deutschland-3-liga",
    ]

    all_matches = []
    for url in urls:

        # retrieve html code and load into bs4
        soup = bs4.BeautifulSoup(requests.get(url).text, "html.parser")

        # loop through all div elements (which are basically all elements)
        for n, div in enumerate(soup.find_all("div")):

            # all div elements with position attribute, which is a match
            if has_attribute(div, "position", ""):

                # derive if it is finished
                stati = div.find_all("div", {"class": "match-status"})
                if len(stati) != 1:
                    raise ScrapingError("More than one match-status found")
                is_finished: bool = stati[0].text.lower() == "beendet"

                # derive start time, it is retrieved as UTC
                start_time: str = div["data-datetime"]
                start_datetime: datetime = datetime.strptime(
                    start_time, "%Y-%m-%dT%H:%M:%SZ"
                )

                all_matches.append((start_datetime, is_finished))
    return all_matches


def has_attribute(elem: bs4.element.Tag, attr_name: str, attr_value: str):
    """
    Identifies beautifulsoup tags with an exact attribute_name and will check
    if attribute_content is contained within the value of the attribute.
    Everything is case-sensitive.
    """

    if attr_name not in elem.attrs.keys():
        return False

    actual_value = " ".join(elem.attrs[attr_name])
    if attr_value in actual_value:
        return True

    return False


def scrape_sportschau_ranking() -> list[str]:
    """
    Returns a list of team names that represent the concatenated rankings
    of 1. Bundesliga, 2. Bundesliga and 3. Bundesliga
    """

    urls = [
        "https://www.sportschau.de/live-und-ergebnisse/fussball/deutschland-bundesliga/tabelle",
        "https://www.sportschau.de/live-und-ergebnisse/fussball/deutschland-2-bundesliga/tabelle",
        "https://www.sportschau.de/live-und-ergebnisse/fussball/deutschland-3-liga/tabelle",
    ]

    ranks = []

    for url in urls:

        # retrieve html code and load into bs4
        soup = bs4.BeautifulSoup(requests.get(url).text, "html.parser")

        for td in soup.find_all("td"):

            try:
                class_str = td["class"]
            except KeyError:
                class_str = []

            s = " ".join(class_str)

            if "team-name" in s.lower():
                ranks.append(td.a.text)

    if len(set(ranks)) != 56:
        raise ScrapingError("Ranking Incomplete")

    return ranks
