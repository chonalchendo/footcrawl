import pydantic as pdt


class Clubs(pdt.BaseModel):
    league: str = pdt.Field(...)
    season: int = pdt.Field(...)
    tm_team_name: list[str] = pdt.Field(...)
    tm_team_id: list[int] = pdt.Field(...)
    team_name: list[str] = pdt.Field(...)
