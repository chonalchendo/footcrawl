import typing as T

import bs4

from footcrawl import metrics, schemas
from footcrawl.parsers import base

if T.TYPE_CHECKING:
    import aiohttp


class CompetitionsParser(base.Parser):
    @T.override
    async def parse(
        self, response: "aiohttp.ClientResponse"
    ) -> T.AsyncGenerator[base.Item, None]:
        content = await response.text()
        soup = bs4.BeautifulSoup(content, "html.parser")

        table = soup.find("table", class_="items")
        rows = table.find_all(["tr", "td"], class_=["extrarow", "odd", "even"])

        for row in rows:
            if "extrarow" in row["class"]:
                tier = row.text
                continue

            data = self._parsers(row)
            data.update({"tier": tier})

            valid_data = self._validate(data, validator=schemas.CompetitionsSchema)
            yield valid_data

    def _parsers(self, row: bs4.Tag) -> base.Item:
        return {
            **self._comp_info(row),
            **self._comp_stats(row),
            **self._comp_values(row),
        }

    def _comp_info(self, row: bs4.Tag) -> base.SubItem:
        link = row.find("a").get("href")
        split_link = link.split("/")
        tm_comp = split_link[1]
        tm_id = split_link[4]
        name = row.find("img").get("alt")

        return {
            "comp_name": name,
            "comp_tm_name": tm_comp,
            "comp_id": tm_id,
            "link": link,
        }

    def _comp_stats(self, row: bs4.Tag) -> base.SubItem:
        stats = row.find_all("td", class_="zentriert")
        country = stats[0].find("img")["alt"]
        clubs = stats[1].text
        players = stats[2].text
        avg_age = stats[3].text
        foreigners = stats[4].text
        game_ratio_of_foreigners = stats[5].text
        goals_per_match = stats[6].text

        return {
            "country": country,
            "clubs": clubs,
            "players": players,
            "avg_age": avg_age,
            "foreigners": foreigners,
            "game_ratio_of_foreigners": game_ratio_of_foreigners,
            "goals_per_match": goals_per_match,
        }

    def _comp_values(self, row: bs4.Tag) -> base.SubItem:
        values = row.find_all("td", class_="rechts")
        avg_market_value = values[0].text
        total_market_value = values[1].text

        return {
            "avg_market_value": avg_market_value,
            "total_market_value": total_market_value,
        }

    @T.override
    @property
    def get_metrics(self) -> metrics.MetricsDict:
        metrics_ = metrics.ParserMetrics(items_parsed=self.__total_items)
        return metrics_.summary()
