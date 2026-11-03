"""Build chronological, player-order-neutral pre-match ATP features."""

from __future__ import annotations

from collections import defaultdict, deque
from pathlib import Path

import numpy as np
import pandas as pd

SURFACES = {"Hard", "Clay", "Grass", "Carpet"}
FEATURES = [
    "elo_diff", "surface_elo_diff", "rank_advantage", "career_winrate_diff",
    "surface_winrate_diff", "recent_10_winrate_diff", "experience_diff",
    "service_points_won_diff", "return_points_won_diff",
]


def expected_score(a: float, b: float) -> float:
    """Classical Elo win probability."""
    return 1.0 / (1.0 + 10.0 ** ((b - a) / 400.0))


def _state() -> dict:
    return {"elo": 1500.0, "surface_elo": defaultdict(lambda: 1500.0),
            "matches": 0, "wins": 0, "surface_matches": defaultdict(int),
            "surface_wins": defaultdict(int), "recent": deque(maxlen=10),
            "serve_won": 0.0, "serve_total": 0.0,
            "return_won": 0.0, "return_total": 0.0}


def _rate(num: float, den: float) -> float:
    return num / den if den else np.nan


def _snapshot(state: dict, surface: str, rank: float) -> dict:
    return {
        "elo": state["elo"], "surface_elo": state["surface_elo"][surface],
        "rank": rank, "career_winrate": _rate(state["wins"], state["matches"]),
        "surface_winrate": _rate(state["surface_wins"][surface], state["surface_matches"][surface]),
        "recent_10_winrate": np.mean(state["recent"]) if state["recent"] else np.nan,
        "experience": np.log1p(state["matches"]),
        "service_points_won": _rate(state["serve_won"], state["serve_total"]),
        "return_points_won": _rate(state["return_won"], state["return_total"]),
    }


def load_main_draw(files: list[Path]) -> pd.DataFrame:
    """Read Jeff Sackmann main-draw ATP CSV files from a user-supplied directory."""
    if not files:
        raise ValueError("No atp_matches_YYYY.csv files found")
    data = pd.concat((pd.read_csv(path, low_memory=False) for path in files), ignore_index=True)
    return data


def build_features(matches: pd.DataFrame) -> pd.DataFrame:
    """Snapshot every match before applying any result from its tournament date.

    Source match statistics only update state after all matches on the same date
    have been snapshotted. This deliberately sacrifices intra-day information.
    """
    required = {"tourney_date", "winner_id", "loser_id", "surface"}
    missing = required - set(matches.columns)
    if missing:
        raise ValueError(f"Missing columns: {sorted(missing)}")
    frame = matches.copy()
    frame["date"] = pd.to_datetime(frame["tourney_date"].astype(str), format="%Y%m%d", errors="coerce")
    frame["winner_id"] = pd.to_numeric(frame["winner_id"], errors="coerce")
    frame["loser_id"] = pd.to_numeric(frame["loser_id"], errors="coerce")
    frame = frame.loc[frame["date"].notna() & frame["surface"].isin(SURFACES)
                      & frame["winner_id"].notna() & frame["loser_id"].notna()].copy()
    if "round" in frame:
        frame = frame.loc[~frame["round"].astype(str).str.match(r"^(Q\d*|QF?L|RRQ)$", case=False)].copy()
    frame["winner_id"] = frame["winner_id"].astype(int)
    frame["loser_id"] = frame["loser_id"].astype(int)
    frame = frame.loc[frame["winner_id"] != frame["loser_id"]]
    frame = frame.sort_values(["date", "winner_id", "loser_id"], kind="stable")
    players = defaultdict(_state)
    result = []
    for date, daily in frame.groupby("date", sort=True):
        for _, match in daily.iterrows():
            winner, loser = match["winner_id"], match["loser_id"]
            a, b = sorted((winner, loser))
            surface = match["surface"]
            ranks = {winner: pd.to_numeric(match.get("winner_rank"), errors="coerce"),
                     loser: pd.to_numeric(match.get("loser_rank"), errors="coerce")}
            sa, sb = _snapshot(players[a], surface, ranks[a]), _snapshot(players[b], surface, ranks[b])
            features = {f"{name}_diff": sa[name] - sb[name]
                        for name in ("elo", "surface_elo", "career_winrate", "surface_winrate",
                                     "recent_10_winrate", "experience", "service_points_won", "return_points_won")}
            features["rank_advantage"] = sb["rank"] - sa["rank"]
            result.append({"date": date, "surface": surface, "player_a": a,
                           "player_b": b, "target": int(a == winner), **features})
        for _, match in daily.iterrows():
            w, l, surface = match["winner_id"], match["loser_id"], match["surface"]
            sw, sl = players[w], players[l]
            ew = expected_score(sw["elo"], sl["elo"])
            es = expected_score(sw["surface_elo"][surface], sl["surface_elo"][surface])
            kw = 40 if sw["matches"] < 30 else 24 if sw["matches"] > 200 else 32
            kl = 40 if sl["matches"] < 30 else 24 if sl["matches"] > 200 else 32
            sw["elo"] += kw * (1 - ew)
            sl["elo"] -= kl * (1 - ew)
            sw["surface_elo"][surface] += kw * (1 - es)
            sl["surface_elo"][surface] -= kl * (1 - es)
            for state, won, own, opponent in ((sw, 1, "w", "l"), (sl, 0, "l", "w")):
                state["matches"] += 1
                state["wins"] += won
                state["surface_matches"][surface] += 1
                state["surface_wins"][surface] += won
                state["recent"].append(won)
                svpt = pd.to_numeric(match.get(f"{own}_svpt"), errors="coerce")
                first_in = pd.to_numeric(match.get(f"{own}_1stIn"), errors="coerce")
                first_won = pd.to_numeric(match.get(f"{own}_1stWon"), errors="coerce")
                second_won = pd.to_numeric(match.get(f"{own}_2ndWon"), errors="coerce")
                opponent_svpt = pd.to_numeric(match.get(f"{opponent}_svpt"), errors="coerce")
                opponent_first_won = pd.to_numeric(match.get(f"{opponent}_1stWon"), errors="coerce")
                opponent_second_won = pd.to_numeric(match.get(f"{opponent}_2ndWon"), errors="coerce")
                if all(pd.notna(x) for x in (svpt, first_in, first_won, second_won)) and svpt > 0:
                    state["serve_total"] += svpt
                    state["serve_won"] += first_won + second_won
                if all(pd.notna(x) for x in (opponent_svpt, opponent_first_won, opponent_second_won)) and opponent_svpt > 0:
                    state["return_total"] += opponent_svpt
                    state["return_won"] += opponent_svpt - opponent_first_won - opponent_second_won
    return pd.DataFrame(result, columns=["date", "surface", "player_a", "player_b", "target", *FEATURES])
