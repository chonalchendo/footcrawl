import typing as T
from collections import defaultdict
from enum import Enum
import re

import bs4

from footcrawl import metrics as metrics_
from footcrawl import schemas
from footcrawl.parsers import base
from footcrawl.parsers.utils import convert_px_to_minute

if T.TYPE_CHECKING:
    import aiohttp

METADATA = 0


class Actions(Enum):
    GOALS = "Goals"
    SUBS = "Substitutions"
    CARDS = "Cards"


def get_action_minute(action: bs4.Tag) -> dict[str, int | None]:
    style = action.find("span", class_="sb-sprite-uhr-klein").get("style")
    pattern = r"background-position:\s*(-?\d+)px\s+(-?\d+)px"
    match = re.search(pattern, style)

    if not match:
        print("No background position found")
        return {"time": None}

    x_pos = int(match.group(1))
    y_pos = int(match.group(2))
    time = convert_px_to_minute(x_pos, y_pos)
    return {"time": time}


class MatchActionsParser(base.Parser):
    @T.override
    async def parse(
        self, response: "aiohttp.ClientResponse"
    ) -> T.AsyncGenerator[base.Item, None]:
        content = await response.text()
        soup = bs4.BeautifulSoup(content, "html.parser")

        boxes = soup.find_all("div", class_="box")

        data = defaultdict(list)
        for i, box in enumerate(boxes):
            if i == METADATA:
                metadata = self._get_metadata(box)
                data.update(metadata)
                continue

            title = box.find("h2", class_="content-box-headline").text.strip()

            if title == Actions.GOALS.value:
                goal_actions = self._get_actions(box)
                for action in goal_actions:
                    goal_handler = GoalAction(action)
                    data["goals"].append(goal_handler.get_goal_action)

            if title == Actions.SUBS.value:
                sub_actions = self._get_actions(box)
                for action in sub_actions:
                    sub_handler = SubAction(action)
                    data["substitutions"].append(sub_handler.get_sub_action)

            if title == Actions.CARDS.value:
                card_actions = self._get_actions(box)
                for action in card_actions:
                    card_handler = CardAction(action)
                    data["cards"].append(card_handler.get_card_action)

        if "goals" not in data:
            data["goals"] = []

        if "substitutions" not in data:
            data["substitutions"] = []

        if "cards" not in data:
            data["cards"] = []

        valid_data = self._validate(
            data=dict(data), validator=schemas.MatchActionsSchema
        )
        self.__total_items = 1
        yield valid_data

    def _get_metadata(self, box: bs4.Tag) -> dict[str, str | int]:
        comp_name = box.find("img")["alt"]
        info = box.find("span", class_="oddsServe")
        comp_id = info["data-competition"]
        matchday = info["data-gameday"]
        match_id = info["data-match"]

        team_url_split = box.find("a")["href"].split("/")
        comp_tm_name = team_url_split[1]
        season = team_url_split[-1]

        return {
            "match_id": match_id,
            "matchday": matchday,
            "comp_id": comp_id,
            "comp_name": comp_name,
            "comp_tm_name": comp_tm_name,
            "season": season,
        }

    @staticmethod
    def _get_actions(box: bs4.Tag) -> bs4.Tag:
        return box.find_all("div", class_="sb-aktion")

    @T.override
    @property
    def get_metrics(self) -> metrics_.MetricsDict:
        metrics = metrics_.ParserMetrics(items_parsed=self.__total_items)
        return metrics.summary()


class GoalAction:
    def __init__(self, box: bs4.Tag) -> None:
        self._box = box
        self._goal_action = self._parse_goal_action(self._box)

    @property
    def get_goal_action(self) -> dict:
        return self._goal_action

    def _parse_goal_action(self, box: bs4.Tag) -> dict:
        return {
            **self._get_club_info(box),
            **self._get_goal_info(box),
            **self._get_assist_info(box),
            **self._get_score_at_time_of_goal(box),
            **get_action_minute(box)
        }

    def _get_club_info(self, box: bs4.Tag):
        club_name = box.find_all("a")[-1]["title"].strip()
        club_href_split = box.find_all("a")[-1]["href"].split("/")
        club_tm_name, club_id = club_href_split[1], club_href_split[4]
        return {
            "club_id": club_id,
            "club_tm_name": club_tm_name,
            "club_name": club_name,
        }

    def _get_goal_info(self, box: bs4.Tag) -> dict[str, str | int]:
        scorer_id, _ = self._get_scorer_assister_ids(box)
        goal, _ = self._get_goal_and_assist(box)
        split_info = goal.split(", ")

        season_total = split_info[2].split(".")[0] if len(split_info) == 3 else None

        return {
            "scorer_id": scorer_id,
            "scorer": split_info[0],
            "shot_type": split_info[1].strip(),
            "scorer_goal_season_total": season_total,
        }

    def _get_assist_info(self, box: bs4.Tag) -> dict[str, str | int | None]:
        _, assister_id = self._get_scorer_assister_ids(box)
        _, assist = self._get_goal_and_assist(box)

        if not assist:
            return {
                "assister_id": None,
                "assister": None,
                "assist_type": None,
                "assister_assist_season_total": None,
            }

        split_info = assist.split(", ")

        assister = split_info[0]
        assist_type = split_info[1] if len(split_info) == 3 else None
        assist_total = split_info[2].split(".")[0] if len(split_info) == 3 else None

        return {
            "assister_id": assister_id,
            "assister": assister,
            "assist_type": assist_type,
            "assister_assist_season_total": assist_total,
        }

    def _get_score_at_time_of_goal(self, box: bs4.Tag) -> dict[str, str | None]:
        score: str = box.find("div", class_="sb-aktion-spielstand").text.strip()
        return {"score": score}

    def _get_scorer_assister_ids(self, box: bs4.Tag):
        items = box.find_all("a", class_="wichtig")
        ids = [href["href"].split("/")[4] for href in items]

        if len(ids) == 1:
            scorer_id = ids[0]
            return scorer_id, None

        scorer_id = ids[0]
        assister_id = ids[1]
        return scorer_id, assister_id

    def _get_goal_and_assist(self, box: bs4.Tag) -> tuple[str, str]:
        text: str = box.find("div", class_="sb-aktion-aktion").text.strip()
        split_text = text.split("Assist:")

        if len(split_text) == 1:
            goal = split_text[0]
            return goal, None

        goal, assist = split_text
        return goal, assist


class SubAction:
    def __init__(self, box: bs4.Tag) -> None:
        self._box = box
        self._sub_action = self._parse_sub_action(self._box)

    @property
    def get_sub_action(self) -> dict[str, str]:
        return self._sub_action

    def _parse_sub_action(self, box: bs4.Tag):
        return {
            **self._get_club_info(box),
            **self._get_player_off_info(box),
            **self._get_player_on_info(box),
            **self._get_sub_reason(box),
            **get_action_minute(box)
        }

    def _get_player_on_info(self, box: bs4.Tag) -> dict[str, str]:
        content = self._get_player_on_content(box)
        player_on = content.text.strip()
        player_on_url = content["href"].split("/")
        player_on_id = player_on_url[4]
        player_on_tm_name = player_on_url[1]
        return {
            "player_on_id": player_on_id,
            "player_on_tm_name": player_on_tm_name,
            "player_on_name": player_on,
        }

    def _get_player_off_info(self, box: bs4.Tag) -> dict[str, str]:
        content = self._get_player_off_content(box)
        player_off = content.text.strip()
        player_off_url = content["href"].split("/")
        player_off_id = player_off_url[4]
        player_off_tm_name = player_off_url[1]
        return {
            "player_off_id": player_off_id,
            "player_off_tm_name": player_off_tm_name,
            "player_off_name": player_off,
        }

    def _get_club_info(self, box: bs4.Tag) -> dict[str, str]:
        content = self._get_club_content(box)
        club = content["title"]
        club_url = content["href"].split("/")
        club_id = club_url[4]
        club_tm_name = club_url[1]
        return {"club_id": club_id, "club_tm_name": club_tm_name, "club_name": club}

    def _get_sub_reason(self, box: bs4.Tag) -> dict[str, str]:
        reason = box.find("span", class_="hide-for-small").text.strip()
        return {"reason": reason}

    def _get_player_on_content(self, box: bs4.Tag) -> bs4.Tag:
        return box.find("span", class_="sb-aktion-wechsel-ein").find("a")

    def _get_player_off_content(self, box: bs4.Tag) -> bs4.Tag:
        return box.find("span", class_="sb-aktion-wechsel-aus").find("a")

    def _get_club_content(self, box: bs4.Tag) -> bs4.Tag:
        return box.find("div", class_="sb-aktion-wappen").find("a")


class CardAction:
    def __init__(self, box: bs4.Tag) -> None:
        self._box = box
        self._card_action = self._parse_card_action(self._box)

    @property
    def get_card_action(self) -> dict:
        return self._card_action

    def _parse_card_action(self, box: bs4.Tag):
        return {
            **self._get_club_info(box),
            **self._get_player_info(box),
            **self._get_card_info(box),
            **get_action_minute(box)
        }

    def _get_player_info(self, box: bs4.Tag) -> dict[str, str]:
        player = box.find("a", class_="wichtig").text.strip()
        player_url = (
            box.find("div", class_="sb-aktion-spielerbild").find("a")["href"].split("/")
        )
        player_id = player_url[4]
        player_tm_name = player_url[1]

        return {
            "player_id": player_id,
            "player_tm_name": player_tm_name,
            "player_name": player,
        }

    def _get_card_info(self, box: bs4.Tag) -> dict[str, str]:
        content = self._get_card_content(box)
        card_info = content.text.strip()
        card_info = " ".join(card_info.split())
        card_info = card_info.split(" ")

        # initialise card count
        card_of_season = None

        for item in card_info:
            if item.replace(".", "").isdigit():
                card_of_season = item.replace(".", "")

            if item.lower() in ["yellow", "red"]:
                card_type = item

        reason = card_info[-1]

        return {
            "card_type": card_type,
            "reason": reason,
            "player_card_type_season_total": card_of_season,
        }

    def _get_club_info(self, box: bs4.Tag) -> dict[str, str]:
        content = self._get_club_content(box)
        club = content["title"]
        club_url = content["href"].split("/")
        club_id = club_url[4]
        club_tm_name = club_url[1]
        return {"club_id": club_id, "club_tm_name": club_tm_name, "club_name": club}

    def _get_card_content(self, box: bs4.Tag) -> bs4.Tag:
        return box.find("div", class_="sb-aktion-aktion")

    def _get_club_content(self, box: bs4.Tag) -> bs4.Tag:
        return box.find("div", class_="sb-aktion-wappen").find("a")
