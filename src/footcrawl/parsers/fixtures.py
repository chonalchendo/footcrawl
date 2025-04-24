import re
import typing as T
from urllib.parse import urlparse

import bs4

from footcrawl import metrics as metrics_
from footcrawl import schemas
from footcrawl.parsers import base

if T.TYPE_CHECKING:
    import aiohttp


class FixturesParser(base.Parser):
    @T.override
    async def parse(
        self, response: "aiohttp.ClientResponse"
    ) -> T.AsyncGenerator[base.Item, None]:
        content = await response.text()
        soup = bs4.BeautifulSoup(content, "html.parser")

        url = response.url
        season = urlparse(str(url)).path.split("/")[6]
        league_id = urlparse(str(url)).path.split("#")[-1]

        index = self._get_table_index(season=season, league_id=league_id)

        boxes = soup.find_all("div", class_="box")[index:]

        for box in boxes:
            comp_id = self._get_competition_id(box)
            comp_tm_name = self._get_competition_tm_name(box)
            comp_name = self._get_competition_name(box)
            club_tm_name = self._get_club_name(box)
            club_id = self._get_club_id(box)

            metadata = {
                "comp_id": comp_id,
                "comp_tm_name": comp_tm_name,
                "comp_name": comp_name,
                "club_tm_name": club_tm_name,
                "club_id": club_id,
            }

            table = self._get_table(box)

            self.__total_items = len(table)

            for fixture in table:
                data = self._parsers(fixture)
                data.update(metadata)
                valid_data = self._validate(data=data, validator=schemas.FixturesSchema)
                yield valid_data

    def _parsers(self, row: bs4.Tag) -> base.Item:
        return {
            **self._get_fixtures_stats(row),
            **self._get_team_manager(row),
            **self._get_match_attendance(row),
            **self._get_team_league_positions(row),
        }

    def _get_table(self, box: bs4.Tag) -> str:
        responsive_tab = box.find("div", class_="responsive-table")
        table = responsive_tab.find_all("tr")[1:]
        return table

    def _get_table_index(self, season: str, league_id: str) -> int:
        if int(season) == 2024 or league_id == "FR1":
            return 3
        return 2

    def _get_competition_name(self, box: bs4.Tag) -> str:
        return box.find("img")["alt"]

    def _get_competition_tm_name(self, box: bs4.Tag) -> str:
        return box.find("a")["href"].split("/")[1]

    def _get_competition_id(self, box: bs4.Tag) -> str:
        return box.find("a")["href"].split("/")[4]

    def _get_club_name(self, box: bs4.Tag) -> str:
        return box.find("a", class_="tm-tab")["href"].split("/")[1]

    def _get_club_id(self, box: bs4.Tag) -> str:
        return box.find("a", class_="tm-tab")["href"].split("/")[4]

    def _get_team_manager(self, row: bs4.Tag) -> base.SubItem:
        manager = row.find_all("a")[-2]["title"]
        return {"manager": manager}

    def _get_match_attendance(self, row: bs4.Tag) -> base.SubItem:
        attendance = row.find("td", class_="rechts").text.strip()
        return {"attendance": attendance}

    def _get_team_league_positions(self, row: bs4.Tag) -> tuple[str | None, str | None]:
        league_positions = row.find_all("td", class_="no-border-links")

        pattern = r"\(([1-9]|1[0-9]|20)\.\)"

        home_team_pos = league_positions[0].text.strip()
        away_team_pos = league_positions[1].text.strip()

        # Search for the pattern in the string
        home_match = re.search(pattern, home_team_pos)
        away_match = re.search(pattern, away_team_pos)

        home_team_league_position = (
            home_team_pos.split(" (")[1].split(".)")[0] if home_match else None
        )
        away_team_league_position = (
            away_team_pos.split(" (")[1].split(".)")[0] if away_match else None
        )
        return {
            "home_team_league_position": home_team_league_position,
            "away_team_league_position": away_team_league_position,
        }

    def _get_fixtures_stats(self, row: bs4.Tag) -> base.SubItem:
        stats = row.find_all("td", class_="zentriert")

        match_date = self._get_match_date(stats)
        match_time = self._get_match_time(stats)
        home_club = self._get_home_club(stats)
        home_club_tm = self._get_home_club_tm_name(stats)
        away_club_tm = self._get_away_club_tm_name(stats)
        away_club = self._get_away_club(stats)
        formation = self._get_formation(stats)
        match_report_url = self._get_match_report_url(stats)
        match_result = self._get_match_result(stats)
        match_id = self._get_match_id(stats)
        matchday = self._get_matchday(stats)

        return {
            "match_id": match_id,
            "matchday": matchday,
            "match_date": match_date,
            "match_time": match_time,
            "home_club_tm": home_club_tm,
            "home_club": home_club,
            "away_club_tm": away_club_tm,
            "away_club": away_club,
            "formation": formation,
            "match_report_url": match_report_url,
            "match_result": match_result,
        }

    def _get_matchday(self, stats: list[bs4.Tag]):
        return stats[0].text.strip()

    def _get_match_date(self, stats: list[bs4.Tag]) -> str:
        return stats[1].text.strip()

    def _get_match_time(self, stats: list[bs4.Tag]) -> str:
        return stats[2].text.strip()

    def _get_home_club(self, stats: list[bs4.Tag]) -> str:
        return stats[3].find("img")["alt"]

    def _get_home_club_tm_name(self, stats: list[bs4.Tag]) -> str:
        return stats[3].find("a")["href"].split("/")[1]

    def _get_away_club_tm_name(self, stats: list[bs4.Tag]) -> str:
        return stats[4].find("a")["href"].split("/")[1]

    def _get_away_club(self, stats: list[bs4.Tag]) -> str:
        return stats[4].find("img")["alt"]

    def _get_formation(self, stats: list[bs4.Tag]) -> str:
        return stats[5].text.strip()

    def _get_match_report_url(self, stats: list[bs4.Tag]) -> str:
        return stats[6].find("a")["href"]

    def _get_match_result(self, stats: list[bs4.Tag]) -> str:
        return stats[6].text.strip()

    def _get_match_id(self, stats: list[bs4.Tag]) -> str:
        match_report_url = self._get_match_report_url(stats)
        return match_report_url.split("/")[4]

    @T.override
    @property
    def get_metrics(self) -> metrics_.MetricsDict:
        metrics = metrics_.ParserMetrics(items_parsed=self.__total_items)
        return metrics.summary()
