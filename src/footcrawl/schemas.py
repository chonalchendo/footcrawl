from __future__ import annotations

import pydantic as pdt


class CompetitionsSchema(pdt.BaseModel):
    comp_name: str
    comp_tm_name: str
    comp_id: str
    link: str
    country: str
    tier: str
    clubs: int
    players: str
    avg_age: float
    foreigners: str
    game_ratio_of_foreigners: str
    goals_per_match: str
    avg_market_value: str
    total_market_value: str


class ClubsSchema(pdt.BaseModel):
    """A Pydantic class to validate parsed clubs data."""

    club_id: int
    club_tm_name: str
    club: str
    club_link: str
    season: int
    comp_id: str
    comp_tm_name: str
    squad_size: int
    average_age: float
    foreign_players: int
    average_player_value: str
    total_player_value: str


class SquadsSchema(pdt.BaseModel):
    player_id: int
    player_tm_name: str
    player_name: str
    club_name: str
    season: int
    url: str
    position: str
    link: str
    injury_note: str | None
    market_value: str
    previous_value: str | None
    number: str
    dob: str
    age: int
    nationalities: list[str]
    height: str | None
    foot: str | None
    signed_date: str | None
    transfer_fee: str | None
    signed_from: str | None
    contract_expiry: str | None


class FixturesSchema(pdt.BaseModel):
    match_id: int
    matchday: int | str
    match_date: str
    match_time: str
    comp_id: str
    comp_tm_name: str
    comp_name: str
    club_id: int
    season: int
    club_tm_name: str
    home_club_tm: str
    home_club: str
    away_club_tm: str
    away_club: str
    formation: str
    match_report_url: str
    match_result: str
    home_team_league_position: str | None
    away_team_league_position: str | None
    attendance: float | str
    manager: str


class MatchLineupsSchema(pdt.BaseModel):
    match_id: int
    matchday: int
    comp_id: str
    comp_name: str
    club_id: int
    club_name: str
    club_tm_name: str
    player_id: int
    player_tm_name: str
    player_name: str
    number: int
    position: str
    current_value: str | None
    country: str
    misc: str | None
    profile_link: str
    season_stats_link: str
    is_starter: bool


class MatchActionsSchema(pdt.BaseModel):
    match_id: int
    matchday: int
    comp_id: str
    comp_name: str
    comp_tm_name: str
    season: int
    goals: list[_GoalAction]
    substitutions: list[_SubAction]
    cards: list[_CardAction]


class _GoalAction(pdt.BaseModel):
    club_id: int
    club_tm_name: str
    club_name: str
    score: str
    scorer: str
    scorer_id: int
    shot_type: str
    scorer_goal_season_total: int | None
    assister: str | None
    assister_id: int | None
    assist_type: str | None
    assister_assist_season_total: int | None
    time: int | None


class _SubAction(pdt.BaseModel):
    club_id: int
    club_tm_name: str
    club_name: str
    reason: str
    player_off_id: int
    player_off_tm_name: str
    player_off_name: str
    player_on_id: int
    player_on_tm_name: str
    player_on_name: str
    time: int | None


class _CardAction(pdt.BaseModel):
    club_id: int
    club_tm_name: str
    club_name: str
    player_id: int
    player_name: str
    player_tm_name: str
    card_type: str
    reason: str
    player_card_type_season_total: int | None
    time: int | None


class MatchStatsSchema(pdt.BaseModel):
    match_id: int
    matchday: int
    comp_id: str
    comp_tm_name: str
    season: int
    home_team_stats: _StatsSchema
    away_team_stats: _StatsSchema


class _StatsSchema(pdt.BaseModel):
    club_id: int | None
    club_tm_name: str | None
    total_shots: int | None
    shots_off_target: int | None
    shots_saved: int | None
    corners: int | None
    free_kicks: int | None
    fouls: int | None
    offsides: int | None


SchemaKind = (
    ClubsSchema
    | SquadsSchema
    | FixturesSchema
    | MatchLineupsSchema
    | MatchActionsSchema
    | MatchStatsSchema
)
