import typing as T
from urllib.parse import urlparse

import bs4

from footcrawl import metrics, schemas
from footcrawl.parsers import base

if T.TYPE_CHECKING:
    import aiohttp


class ClubsParser(base.Parser):
    @T.override
    async def parse(
        self, response: "aiohttp.ClientResponse"
    ) -> T.AsyncGenerator[base.Item, None]:
        content = await response.text()
        soup = bs4.BeautifulSoup(content, "html.parser")

        table = soup.find_all(class_="items")
        rows = table[0].find_all("tr", class_=["odd", "even"])

        self.__total_items = len(rows)

        url = response.url
        split_comp_url = urlparse(str(url)).path.split("/")
        comp_name = split_comp_url[1]
        comp_id = split_comp_url[4]

        metadata = {"comp_tm_name": comp_name, "comp_id": comp_id}

        for row in rows:
            data = self._parsers(row)
            data.update(metadata)

            valid_data = self._validate(data, validator=schemas.ClubsSchema)
            yield valid_data

    @T.override
    def _parsers(self, row: bs4.Tag) -> base.Item:
        return {
            **self._get_club_name(row),
            **self._get_club_stats(row),
            **self._get_club_values(row),
        }

    def _get_club_name(self, row: bs4.Tag) -> base.SubItem:
        name = row.find("td", class_="hauptlink").text.strip()
        return {"club": name}

    def _get_club_stats(self, row: bs4.Tag) -> base.SubItem:
        stats = row.find_all("td", class_="zentriert")
        squad_size = stats[1].text
        # team link
        link = stats[1].find("a")["href"]
        # tm name
        tm_name = link.split("/")[1]
        # tm id
        tm_id = link.split("/")[4]
        # season
        season = link.split("/")[6]
        # average age
        avg_age = stats[2].text
        # foreign players
        foreign_players = stats[3].text

        return {
            "squad_size": squad_size,
            "average_age": avg_age,
            "foreign_players": foreign_players,
            "club_link": link,
            "club_tm_name": tm_name,
            "club_id": tm_id,
            "season": season,
        }

    def _get_club_values(self, row: bs4.Tag) -> base.SubItem:
        values = row.find_all("td", class_="rechts")

        avg_player_value = values[0].text.strip()
        total_player_value = values[1].text.strip()

        return {
            "average_player_value": avg_player_value,
            "total_player_value": total_player_value,
        }

    @T.override
    @property
    def get_metrics(self) -> metrics.MetricsDict:
        metrics_ = metrics.ParserMetrics(items_parsed=self.__total_items)
        return metrics_.summary()
