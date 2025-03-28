import pydantic as pdt


class ClubsSchema(pdt.BaseModel):
    """A Pydantic class to validate parsed clubs data."""

    club: str = pdt.Field(...)
    squad_size: str = pdt.Field(...)
    average_age: str = pdt.Field(...)
    foreign_players: str = pdt.Field(...)
    season: str = pdt.Field(...)
    average_player_value: str = pdt.Field(...)
    total_player_value: str = pdt.Field(...)
    team_link: str = pdt.Field(...)
    tm_name: str = pdt.Field(...)
    tm_id: str = pdt.Field(...)


SchemaKind = ClubsSchema
