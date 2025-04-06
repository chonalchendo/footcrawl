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


class SquadsSchema(pdt.BaseModel):
    player: str = pdt.Field(...)
    team: str = pdt.Field(...)
    season: str = pdt.Field(...)
    url: str = pdt.Field(...)
    position: str = pdt.Field(...)
    link: str = pdt.Field(...)
    tm_id: str = pdt.Field(...)
    tm_name: str = pdt.Field(...)
    injury_note: str | None = pdt.Field(...)
    market_value: str = pdt.Field(...)
    previous_value: str | None = pdt.Field(...)
    number: str = pdt.Field(...)
    dob: str = pdt.Field(...)
    age: str = pdt.Field(...)
    nationalities: list[str] = pdt.Field(...)
    height: str | None = pdt.Field(...)
    foot: str | None = pdt.Field(...)
    signed_date: str | None = pdt.Field(...)
    transfer_fee: str | None = pdt.Field(...)
    signed_from: str | None = pdt.Field(...)
    contract_expiry: str | None = pdt.Field(...)


SchemaKind = ClubsSchema | SquadsSchema
