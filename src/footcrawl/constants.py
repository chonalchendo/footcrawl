import typing as T

LeagueMap = T.TypedDict(
    "LeagueMap",
    {
        "premier-league": str,
        "la-liga": str,
        "serie-a": str,
        "bundesliga": str,
        "ligue-1": str,
    },
)


LEAGUE_MAP: LeagueMap = {
    "premier-league": "GB1",
    "la-liga": "ES1",
    "serie-a": "IT1",
    "bundesliga": "L1",
    "ligue-1": "FR1",
}
