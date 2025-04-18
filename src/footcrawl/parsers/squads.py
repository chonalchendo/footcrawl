import typing as T
from urllib.parse import urlparse

import bs4

from footcrawl import metrics as metrics_
from footcrawl import schemas
from footcrawl.parsers import base

if T.TYPE_CHECKING:
    import aiohttp


class SquadsParser(base.Parser):
    @T.override
    async def parse(
        self, response: "aiohttp.ClientResponse"
    ) -> T.AsyncGenerator[base.Item, None]:
        content = await response.text()
        soup = bs4.BeautifulSoup(content, "html.parser")

        url = response.url
        split_url = urlparse(str(url)).path.split("/")
        season = split_url[6]
        team = split_url[1]

        metadata = {
            "club_name": team,
            "season": season,
            "url": str(url),
        }

        rows = self._parse_table(soup)
        self.__total_items = len(rows)

        for row in rows:
            data = self._parsers(row, season)
            data.update(metadata)
            valid_data = self._validate(data=data, validator=schemas.SquadsSchema)
            yield valid_data

    @T.override
    def _parsers(self, row: bs4.Tag, season: int) -> base.Item:
        return {
            **self._get_player_profile_link(row),
            **self._get_player_name(row),
            **self._get_player_position(row),
            **self._get_player_injury_note(row, season=season),
            **self._get_player_stats(row, season=season),
            **self._get_market_value(row),
        }

    def _parse_table(self, soup: bs4.BeautifulSoup) -> T.Sequence[str]:
        table = soup.find_all(class_="items")
        rows = table[0].find_all("tr", class_=["odd", "even"])
        return rows

    def _get_player_profile_link(self, row: bs4.Tag) -> base.SubItem:
        link = row.find("td", {"class": "hauptlink"}).find("a")["href"]
        tm_id = link.split("/")[4]
        tm_name = link.split("/")[1]
        return {"link": link, "player_id": tm_id, "player_tm_name": tm_name}

    def _get_player_name(self, row: bs4.Tag) -> base.SubItem:
        name = row.find("td", {"class": "hauptlink"}).find("a").text.strip()
        return {"player_name": name}

    def _get_player_position(self, row: bs4.Tag) -> base.SubItem:
        position = row.find_all("td")[1].text.strip().split("  ")[-1]
        return {"position": position}

    def _get_player_injury_note(self, row: bs4.Tag, season: int) -> base.SubItem:
        injury_note_ = row.find("td", {"class": "hauptlink"}).find("a").find("span")
        injury_note = injury_note_["title"] if injury_note_ and season == 2024 else None
        return {"injury_note": injury_note}

    def _get_market_value(self, row: bs4.Tag) -> base.SubItem:
        value_object = row.find("td", class_="rechts hauptlink")
        # market value
        market_value = value_object.text.strip()
        # previous market value
        previous_value = (
            value_object.find("span")["title"].split(": ")[1]
            if value_object.find("span")
            else None
        )

        return {"market_value": market_value, "previous_value": previous_value}

    def _get_player_stats(self, row: bs4.Tag, season: int) -> base.SubItem:
        stats = row.find_all("td", class_="zentriert")

        number = self._get_player_number(stats)
        dob, age = self._get_player_dob(stats)
        nationalities = self._get_nationalities(stats)
        height = self._get_height(stats, season)
        foot = self._get_foot(stats, season)
        signed_date = self._get_signed_date(stats, season)
        transfer_fee, signed_from = self._get_transfer_data(stats)
        contract_expiry = self._get_contract_expiry(stats)

        return {
            "number": number,
            "dob": dob,
            "age": age,
            "nationalities": nationalities,
            "height": height,
            "foot": foot,
            "signed_date": signed_date,
            "transfer_fee": transfer_fee,
            "signed_from": signed_from,
            "contract_expiry": contract_expiry,
        }

    def _get_player_number(self, stats: list) -> str | None:
        if stats[0].text.strip() == "":
            return None
        return stats[0].text.strip()

    def _get_player_dob(self, stats: list) -> tuple[str, str] | tuple[None, None]:
        if stats[1].text.strip() == "":
            return None, None
        dob = stats[1].text.strip().split(" (")[0]
        age = stats[1].text.strip().split(" (")[1].replace(")", "")
        return dob, age

    def _get_nationalities(self, stats: list) -> list[str] | None:
        if stats[2].find_all("img") == []:
            return None
        return [stat["title"] for stat in stats[2].find_all("img")]

    def _get_height(self, stats: list, season: int) -> str | None:
        if int(season) == 2024:
            return stats[3].text.strip()
        return stats[4].text.strip()

    def _get_foot(self, stats: list, season: int) -> str | None:
        if stats[4].text.strip() == "":
            return None
        if int(season) == 2024:
            return stats[4].text.strip()
        return stats[5].text.strip()

    def _get_signed_date(self, stats: list, season: int) -> str | None:
        if stats[5].text.strip() == "":
            return None
        if int(season) == 2024:
            return stats[5].text.strip()
        return stats[6].text.strip()

    def _get_contract_expiry(self, stats: list) -> str | None:
        if stats[7].text.strip() == "":
            return None
        return stats[7].text.strip()

    def _get_transfer_data(self, stats: list) -> tuple[str | None, str | None]:
        if stats[7].find("a") is None and stats[6].find("a") is None:
            return None, None

        if stats[6].find("a"):
            transfer_fee = stats[6].find("a")["title"].split(": Ablöse ")[1]
            signed_from = stats[6].find("a")["title"].split(": Ablöse ")[0]
            return transfer_fee, signed_from

        transfer_fee = stats[7].find("a")["title"].split(": Ablöse ")[1]
        signed_from = stats[7].find("a")["title"].split(": Ablöse ")[0]
        return transfer_fee, signed_from

    @T.override
    @property
    def get_metrics(self) -> metrics_.MetricsDict:
        metrics = metrics_.ParserMetrics(items_parsed=self.__total_items)
        return metrics.summary()
