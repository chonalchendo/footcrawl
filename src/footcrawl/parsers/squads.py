import bs4
import typing as T

from footcrawl.parsers import base


if T.TYPE_CHECKING:
    import aiohttp

    from footcrawl import metrics


class SquadsParser(base.Parser):
    def parse(self, response: "aiohttp.ClientResponse"):
        content = response.text()
        soup = bs4.BeautifulSoup(content, "html.parser")
        return squads_parser(body=soup, season=self.__season)


def squads_parser(body: str, season: int) -> T.Generator[dict[str, T.Any], None, None]:
    soup = bs4.BeautifulSoup(body, "html.parser")
    rows = parse_table(soup)
    for row in rows:
        yield parse_player_data(row, season)


def parse_table(soup: bs4.BeautifulSoup) -> T.Sequence[str]:
    table = soup.find_all(class_="items")
    rows = table[0].find_all("tr", class_=["odd", "even"])
    return rows


def parse_player_data(row: str, season: int) -> T.Mapping[str, T.Any]:
    return {
        **get_player_profile_link(row),
        **get_player_name(row),
        **get_player_position(row),
        **get_player_injury_note(row, season=season),
        **get_player_stats(row, season=season),
        **get_market_value(row),
    }


def get_player_profile_link(row: str) -> dict[str, T.Any]:
    link = row.find("td", {"class": "hauptlink"}).find("a")["href"]
    tm_id = link.split("/")[4]
    tm_name = link.split("/")[1]
    return {"link": link, "tm_id": tm_id, "tm_name": tm_name}


def get_player_name(row: str) -> dict[str, T.Any]:
    name = row.find("td", {"class": "hauptlink"}).find("a").text.strip()
    return {"player": name}


def get_player_position(row: str) -> dict[str, T.Any]:
    position = row.find_all("td")[1].text.strip().split("  ")[-1]
    return {"position": position}


def get_player_injury_note(row: str, season: int) -> dict[str, T.Any]:
    injury_note_ = row.find("td", {"class": "hauptlink"}).find("a").find("span")
    injury_note = injury_note_["title"] if injury_note_ and season == 2024 else None
    return {"injury_note": injury_note}


def get_market_value(row: str) -> dict[str, T.Any]:
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


def get_player_stats(row: str, season: int) -> dict[str, T.Any]:
    stats = row.find_all("td", class_="zentriert")

    number = _get_player_number(stats)
    dob, age = _get_player_dob(stats)
    nationalities = _get_nationalities(stats)
    height = _get_height(stats, season)
    foot = _get_foot(stats, season)
    signed_date = _get_signed_date(stats, season)
    transfer_fee, signed_from = _get_transfer_data(stats)
    contract_expiry = _get_contract_expiry(stats)

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


def _get_player_number(stats: list) -> str | None:
    if stats[0].text.strip() == "":
        return None
    return stats[0].text.strip()


def _get_player_dob(stats: list) -> str | None:
    if stats[1].text.strip() == "":
        return None
    dob = stats[1].text.strip().split(" (")[0]
    age = stats[1].text.strip().split(" (")[1].replace(")", "")
    return dob, age


def _get_nationalities(stats: list) -> list[str] | None:
    if stats[2].find_all("img") == []:
        return None
    return [stat["title"] for stat in stats[2].find_all("img")]


def _get_height(stats: list, season: int) -> str | None:
    if stats[3].text.strip() == "":
        return None
    if season == 2024:
        return stats[3].text.strip()
    return stats[4].text.strip()


def _get_foot(stats: list, season: int) -> str | None:
    if stats[4].text.strip() == "":
        return None
    if season == 2024:
        return stats[4].text.strip()
    return stats[5].text.strip()


def _get_signed_date(stats: list, season: int) -> str | None:
    if stats[5].text.strip() == "":
        return None
    if season == 2024:
        return stats[5].text.strip()
    return stats[6].text.strip()


def _get_contract_expiry(stats: list) -> str | None:
    if stats[7].text.strip() == "":
        return None
    return stats[7].text.strip()


def _get_transfer_data(stats: list):
    if stats[7].find("a") is None and stats[6].find("a") is None:
        return None, None

    if stats[6].find("a"):
        transfer_fee = stats[6].find("a")["title"].split(": Ablöse ")[1]
        signed_from = stats[6].find("a")["title"].split(": Ablöse ")[0]
        return transfer_fee, signed_from

    transfer_fee = stats[7].find("a")["title"].split(": Ablöse ")[1]
    signed_from = stats[7].find("a")["title"].split(": Ablöse ")[0]
    return transfer_fee, signed_from
