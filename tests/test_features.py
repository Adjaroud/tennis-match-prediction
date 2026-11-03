"""Temporal integrity checks for the public example."""

import pandas as pd

from tennis_portfolio.features import build_features
from tennis_portfolio.style_rule_engine import rank_style_candidates


def _match(date, winner, loser, surface="Hard"):
    return {"tourney_date": date, "winner_id": winner, "loser_id": loser, "surface": surface}


def test_same_day_results_do_not_change_prematch_features():
    data = pd.DataFrame([_match(20240101, 1, 2), _match(20240101, 2, 3)])
    features = build_features(data)
    assert (features["elo_diff"] == 0).all()
    assert (features["surface_elo_diff"] == 0).all()


def test_result_changes_only_later_dates_and_only_played_surface():
    data = pd.DataFrame([_match(20240101, 1, 2), _match(20240102, 2, 1),
                         _match(20240103, 1, 2, "Clay")])
    features = build_features(data)
    assert features.loc[0, "elo_diff"] == 0
    assert features.loc[1, "elo_diff"] > 0
    assert features.loc[1, "surface_elo_diff"] > 0
    assert features.loc[2, "surface_elo_diff"] == 0


def test_swapping_winner_does_not_change_current_match_features():
    first = build_features(pd.DataFrame([_match(20240101, 1, 2)]))
    second = build_features(pd.DataFrame([_match(20240101, 2, 1)]))
    assert first.drop(columns="target").equals(second.drop(columns="target"))
    assert first.loc[0, "target"] != second.loc[0, "target"]


def test_player_order_is_numeric_not_lexicographic():
    features = build_features(pd.DataFrame([_match(20240101, 2, 10)]))
    assert (features.loc[0, "player_a"], features.loc[0, "player_b"]) == (2, 10)


def test_style_rule_selects_server_for_clear_synthetic_case():
    row = {"ace": 94, "serve": 90, "service_games_pct": 88,
           "return_proxy": 35, "ret_games": 30, "matches": 120}
    result = rank_style_candidates(row)
    assert result["primary"] == "BIG_SERVER"
