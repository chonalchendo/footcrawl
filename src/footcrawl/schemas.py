from __future__ import annotations

import pydantic as pdt


class ClubsSchema(pdt.BaseModel):
    """A Pydantic class to validate parsed clubs data."""

    club_id: str = pdt.Field(...)
    club_tm_name: str = pdt.Field(...)
    club: str = pdt.Field(...)
    club_link: str = pdt.Field(...)
    season: str = pdt.Field(...)
    comp_id: str = pdt.Field(...)
    comp_name: str = pdt.Field(...)
    squad_size: str = pdt.Field(...)
    average_age: str = pdt.Field(...)
    foreign_players: str = pdt.Field(...)
    average_player_value: str = pdt.Field(...)
    total_player_value: str = pdt.Field(...)


class SquadsSchema(pdt.BaseModel):
    player_id: str = pdt.Field(...)
    player_tm_name: str = pdt.Field(...)
    player_name: str = pdt.Field(...)
    club_name: str = pdt.Field(...)
    season: str = pdt.Field(...)
    url: str = pdt.Field(...)
    position: str = pdt.Field(...)
    link: str = pdt.Field(...)
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
    comp_id: str = pdt.Field(...)
    comp_tm_name: str = pdt.Field(...)
    comp_name: str = pdt.Field(...)
    club_id: str = pdt.Field(...)
    club_tm_name: str = pdt.Field(...)
    home_club_tm: str = pdt.Field(...)
    home_club: str = pdt.Field(...)
    away_club_tm: str = pdt.Field(...)
    away_club: str = pdt.Field(...)
    formation: str = pdt.Field(...)
    match_report_url: str = pdt.Field(...)
    match_result: str = pdt.Field(...)
    home_team_league_position: str | None = pdt.Field(...)
    away_team_league_position: str | None = pdt.Field(...)
    attendance: str = pdt.Field(...)
    manager: str = pdt.Field(...)


class MatchLineupsSchema(pdt.BaseModel):
    match_id: str = pdt.Field(...)
    matchday: str = pdt.Field(...)
    comp_id: str = pdt.Field(...)
    comp_name: str = pdt.Field(...)
    club_id: str = pdt.Field(...)
    club_name: str = pdt.Field(...)
    club_tm_name: str = pdt.Field(...)
    player_id: str = pdt.Field(...)
    player_tm_name: str = pdt.Field(...)
    player_name: str = pdt.Field(...)
    number: str = pdt.Field(...)
    position: str = pdt.Field(...)
    current_value: str = pdt.Field(...)
    country: str = pdt.Field(...)
    misc: str = pdt.Field(...)
    profile_link: str = pdt.Field(...)
    season_stats_link: str = pdt.Field(...)
    starter: bool = pdt.Field(...)


class MatchActionsSchema(pdt.BaseModel):
    match_id: str
    matchday: str
    comp_id: str
    comp_name: str
    comp_tm_name: str
    season: str
    goals: list[_GoalAction]
    substitutions: list[_SubAction]
    cards: list[_CardAction]


class _GoalAction(pdt.BaseModel):
    club_id: str = pdt.Field(...)
    club_tm_name: str = pdt.Field(...)
    club_name: str = pdt.Field(...)
    score: str = pdt.Field(...)
    scorer: str = pdt.Field(...)
    scorer_id: str = pdt.Field(...)
    shot_type: str = pdt.Field(...)
    scorer_goal_season_total: str = pdt.Field(...)
    assister: str = pdt.Field(...)
    assister_id: str = pdt.Field(...)
    assist_type: str = pdt.Field(...)
    assister_assist_season_total: str = pdt.Field(...)


class _SubAction(pdt.BaseModel):
    club_id: str = pdt.Field(...)
    club_tm_name: str = pdt.Field(...)
    club_name: str = pdt.Field(...)
    reason: str = pdt.Field(...)
    player_off_id: str = pdt.Field(...)
    player_off: str = pdt.Field(...)
    player_on_id: str = pdt.Field(...)
    player_off_id: str = pdt.Field(...)


class _CardAction(pdt.BaseModel):
    club_id: str = pdt.Field(...)
    club_tm_name: str = pdt.Field(...)
    club_name: str = pdt.Field(...)
    player_id: str = pdt.Field(...)
    player_name: str = pdt.Field(...)
    player_tm_name: str = pdt.Field(...)
    card_type: str = pdt.Field(...)
    reason: str = pdt.Field(...)
    player_card_type_season_total: str = pdt.Field(...)


class MatchStatsSchema(pdt.BaseModel):
    match_id: str = pdt.Field(...)
    matchday: str = pdt.Field(...)
    comp_id: str = pdt.Field(...)
    comp_tm_name: str = pdt.Field(...)
    season: str = pdt.Field(...)
    home_team_stats: _StatsSchema
    away_team_stats: _StatsSchema


class _StatsSchema(pdt.BaseModel):
    club_id: str
    club_tm_name: str
    total_shots: str = pdt.Field(...)
    shots_off_target: str = pdt.Field(...)
    shots_saved: str = pdt.Field(...)
    corners: str = pdt.Field(...)
    free_kicks: str = pdt.Field(...)
    fouls: str = pdt.Field(...)
    offsides: str = pdt.Field(...)


SchemaKind = (
    ClubsSchema
    | SquadsSchema
    | FixturesSchema
    | MatchLineupsSchema
    | MatchActionsSchema
    | MatchStatsSchema
)
