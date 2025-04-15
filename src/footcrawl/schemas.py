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
    league: str = pdt.Field(...)
    league_id: str = pdt.Field(...)


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


class FixturesSchema(pdt.BaseModel):
    match_id: str
    match_date: str = pdt.Field(...)
    match_time: str = pdt.Field(...)
    home_team: str = pdt.Field(...)
    away_team: str = pdt.Field(...)
    formation: str = pdt.Field(...)
    match_report_url: str = pdt.Field(...)
    match_result: str = pdt.Field(...)
    home_team_league_position: str | None = pdt.Field(...)
    away_team_league_position: str | None = pdt.Field(...)
    attendance: str = pdt.Field(...)
    manager: str = pdt.Field(...)
    competition: str = pdt.Field(...)
    team: str = pdt.Field(...)


class MatchLineupsSchema(pdt.BaseModel):
    match_id: str = pdt.Field(...)
    team_id: str = pdt.Field(...)
    team: str = pdt.Field(...)
    player_id: str = pdt.Field(...)
    player_tm: str = pdt.Field(...)
    player: str = pdt.Field(...)
    number: str = pdt.Field(...)
    position: str = pdt.Field(...)
    current_value: str = pdt.Field(...)
    country: str = pdt.Field(...)
    misc: str = pdt.Field(...)
    profile_link: str = pdt.Field(...)
    season_stats_link: str = pdt.Field(...)
    starter: bool = pdt.Field(...)


SchemaKind = ClubsSchema | SquadsSchema | FixturesSchema | MatchLineupsSchema
