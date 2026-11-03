"""Run a data-free demonstration using synthetic matches and synthetic style inputs."""

from __future__ import annotations

import pandas as pd

from .features import FEATURES, build_features
from .style_rule_engine import rank_style_candidates
from .style_taxonomy import get_style_label


def main() -> None:
    matches = pd.DataFrame([
        {"tourney_date": 20240101, "surface": "Hard", "winner_id": 101, "loser_id": 202},
        {"tourney_date": 20240101, "surface": "Hard", "winner_id": 202, "loser_id": 303},
        {"tourney_date": 20240108, "surface": "Clay", "winner_id": 202, "loser_id": 101},
    ])
    print("Synthetic pre-match feature preview:")
    print(build_features(matches)[["date", "player_a", "player_b", "target", *FEATURES[:3]]].to_string(index=False))
    synthetic_style_scores = {
        "ace": 94, "serve": 90, "service_games_pct": 88, "return_proxy": 35,
        "ret_games": 30, "matches": 120,
    }
    ranked = rank_style_candidates(synthetic_style_scores)
    print("\nSynthetic style example:", get_style_label(ranked["primary"]))


if __name__ == "__main__":
    main()
