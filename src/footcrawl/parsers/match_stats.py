import typing as T
from collections import defaultdict
from enum import Enum

import bs4

from footcrawl import metrics as metrics_
from footcrawl import schemas
from footcrawl.parsers import base

if T.TYPE_CHECKING:
    import aiohttp


class Index(Enum):
    METADATA = 0
    STATS = 1


class Team(Enum):
    HOME = "heim"
    AWAY = "gast"


class MatchStatsParser(base.Parser):
    @T.override
    async def parse(
        self, response: "aiohttp.ClientResponse"
    ) -> T.AsyncGenerator[base.Item, None]:
        content = await response.text()
        soup = bs4.BeautifulSoup(content, "html.parser")

        boxes = soup.find_all("div", class_="box")[:2]

        data = defaultdict(dict)

        for i, box in enumerate(boxes):
            if i == Index.METADATA.value:
                metadata = self._get_metadata(box)
                data.update(metadata)

            if i == Index.STATS.value:
                stats_exist = self._check_if_stats_exist(box)

                if not stats_exist:
                    null_stats = self._return_null_stats()
                    data.update(null_stats)
                    continue

                stats = self._get_stats(box)
                data.update(stats)

        valid_data = self._validate(data=dict(data), validator=schemas.MatchStatsSchema)
        self.__total_items = 1
        yield valid_data

    @T.override
    @property
    def get_metrics(self) -> metrics_.MetricsDict:
        metrics = metrics_.ParserMetrics(items_parsed=self.__total_items)
        return metrics.summary()

    def _get_metadata(self, box: bs4.Tag) -> dict[str, int | str]:
        match_info = box.find("span", class_="oddsServe")
        comp_id = match_info["data-competition"]
        matchday = match_info["data-gameday"]
        match_id = match_info["data-match"]

        comp_info = box.find("a", class_="direct-headline__link")["href"].split("/")
        comp_tm_name = comp_info[1]
        season = comp_info[6]

        return {
            "match_id": match_id,
            "matchday": matchday,
            "comp_id": comp_id,
            "comp_tm_name": comp_tm_name,
            "season": season,
        }

    def _get_stats(self, box: bs4.Tag) -> dict[dict[str, int | str]]:
        home_team = self._get_team_stats(box, is_home=True)
        away_team = self._get_team_stats(box, is_home=False)
        return {"home_team_stats": home_team, "away_team_stats": away_team}

    def _get_team_stats(self, box: bs4.Tag, is_home: bool) -> dict[str, int | str]:
        team = Team.HOME.value

        if not is_home:
            team = Team.AWAY.value

        team_stats = box.find_all("li", class_=f"sb-statistik-{team}")
        team_url = team_stats[0].find("a")["href"].split("/")
        team_tm_name = team_url[1]
        team_id = team_url[4]

        team_stats_dict = {
            "club_id": team_id,
            "club_tm_name": team_tm_name,
        }

        stat_names = self._get_stats_names(box)
        for stat, name in zip(team_stats, stat_names):
            content = stat.find("div", class_="sb-statistik-zahl").text.strip()
            team_stats_dict.update({name: content})

        return team_stats_dict

    def _get_stats_names(self, box: bs4.Tag) -> list[str]:
        stats_box = box.find_all("div", class_="unterueberschrift")
        return [name.text.strip().lower().replace(" ", "_") for name in stats_box][1:]

    def _check_if_stats_exist(self, box: bs4.Tag) -> bool:
        stats_title: str = box.find("h2", class_="content-box-headline").text.strip()
        if stats_title.lower() != "statistics":
            return False
        return True

    @staticmethod
    def _return_null_stats() -> dict[str, dict[str, None]]:
        stats = {
            "club_id": None,
            "club_tm_name": None,
            "total_shots": None,
            "shots_off_target": None,
            "shots_saved": None,
            "corners": None,
            "free_kicks": None,
            "fouls": None,
            "offsides": None,
        }

        return {"home_team_stats": stats, "away_team_stats": stats}
