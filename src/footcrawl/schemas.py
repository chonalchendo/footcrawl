import pydantic as pdt


class Clubs(pdt.BaseModel):
    league: str = pdt.Field(...)
    season: int = pdt.Field(...)
    tm_team_name: str = pdt.Field(...)
    tm_team_id: int = pdt.Field(...)
    team_name: str = pdt.Field(...)
