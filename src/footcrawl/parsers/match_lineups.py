import typing as T

import bs4

from footcrawl import metrics as metrics_
from footcrawl import schemas
from footcrawl.parsers import base

if T.TYPE_CHECKING:
    import aiohttp


class MatchLineupsParser(base.Parser):
    @T.override
    async def parse(
        self, response: "aiohttp.ClientResponse"
    ) -> T.AsyncGenerator[base.Item, None]:
        content = await response.text()
        soup = bs4.BeautifulSoup(content, "html.parser")

        boxes = soup.find_all("div", class_="box")[:5]

        for i, box in enumerate(boxes):
            if i == 0:
                metadata = self._get_match_metadata(box)
                if not metadata:
                    raise ValueError("Metadata not found in the response.")
                continue

            club_info = self._get_club_info(box)

            # parse lineup content directly
            items = box.find("table", class_="items")
            content = items.find_all("tr")[::3]

            for player in content:
                data = {
                    **metadata,
                    **club_info,
                    **self._parsers(player),
                    **self._get_is_starter(i),
                }

                self.__total_items = 1

                valid_data = self._validate(
                    data=data, validator=schemas.MatchLineupsSchema
                )
                yield valid_data

    def _parsers(self, row: bs4.Tag) -> base.Item:
        return {
            **self._get_player_name(row),
            **self._get_player_profile_info(row),
            **self._get_position_and_value(row),
            **self._get_season_stats_link(row),
            **self._get_squad_number(row),
            **self._get_country(row),
            **self._get_add_info(row),
        }

    def _get_match_metadata(self, box: bs4.Tag) -> dict[str, str]:
        comp_name = box.find("img")["alt"]
        info = box.find("span", class_="oddsServe")
        comp_id = info["data-competition"]
        matchday = info["data-gameday"]
        match_id = info["data-match"]

        return {
            "match_id": match_id,
            "matchday": matchday,
            "comp_id": comp_id,
            "comp_name": comp_name,
        }

    def _get_club_info(self, box: bs4.Tag) -> dict[str, int | str]:
        club_name = box.find("a")["title"]
        href = box.find("a")["href"].split("/")
        club_tm_name = href[1]
        club_id = href[4]
        return {
            "club_id": club_id,
            "club_name": club_name,
            "club_tm_name": club_tm_name,
        }

    def _get_player_name(self, player: bs4.Tag) -> dict[str, str]:
        player_name = player.find("img")["title"]
        return {"player_name": player_name}

    def _get_player_profile_info(self, player: bs4.Tag) -> dict[str, str]:
        profile_link = player.find("a")["href"]
        tm_id = profile_link.split("/")[4]
        tm_name = profile_link.split("/")[1]
        return {
            "profile_link": profile_link,
            "player_id": tm_id,
            "player_tm_name": tm_name,
        }

    def _get_squad_number(self, player: bs4.Tag) -> dict[str, str]:
        number = player.find("div", class_="rn_nummer").text.strip()
        return {"number": number}

    def _get_add_info(self, player: bs4.Tag) -> dict[str, str | None]:
        add_info = player.find("td", class_="neuzugang")
        if not add_info:
            return {"misc": None}
        return {"misc": add_info["title"]}

    def _get_country(self, player: bs4.Tag) -> dict[str, str]:
        country = player.find_all("td", class_="zentriert")[1].find("img")["title"]
        return {"country": country}

    def _get_season_stats_link(self, player: bs4.Tag) -> dict[str, str]:
        season_stats_link = player.find("a", class_="wichtig")["href"]
        return {"season_stats_link": season_stats_link}

    def _get_position_and_value(self, player: bs4.Tag) -> dict[str, str | None]:
        info = player.find_all("td")[-2].text.split(", ")
        if len(info) == 1:
            return {"position": info[0], "current_value": None}
        return {"position": info[0], "current_value": info[1]}

    def _get_is_starter(self, index: int) -> dict[str, bool]:
        is_starter = True if index in [1, 2] else False
        return {"is_starter": is_starter}

    @T.override
    @property
    def get_metrics(self) -> metrics_.MetricsDict:
        metrics = metrics_.ParserMetrics(items_parsed=self.__total_items)
        return metrics.summary()
