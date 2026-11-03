"""Small, reproducible sport-only baseline for the portfolio edition."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, brier_score_loss, log_loss, roc_auc_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from .features import FEATURES, build_features, expected_score, load_main_draw


def evaluate(data_dir: Path) -> dict:
    """Fit on 2000-2019, check 2020-2022, evaluate 2023-2025."""
    files = sorted(data_dir.glob("atp_matches_20[0-2][0-9].csv"))
    files = [p for p in files if 2000 <= int(p.stem[-4:]) <= 2025]
    dataset = build_features(load_main_draw(files))
    year = dataset["date"].dt.year
    train = dataset.loc[year <= 2019]
    validation = dataset.loc[year.between(2020, 2022)]
    test = dataset.loc[year.between(2023, 2025)]
    if min(len(train), len(validation), len(test)) < 20:
        raise ValueError("At least 20 matches are required in each temporal split")
    model = make_pipeline(SimpleImputer(strategy="median", add_indicator=True),
                          StandardScaler(), LogisticRegression(max_iter=1000))
    model.fit(train[FEATURES], train["target"])

    def metrics(split) -> dict:
        truth = split["target"].to_numpy()
        probability = model.predict_proba(split[FEATURES])[:, 1]
        elo = np.array([expected_score(1500 + d / 2, 1500 - d / 2)
                        for d in split["elo_diff"].to_numpy()])
        return {
            "matches": len(split),
            "model_log_loss": float(log_loss(truth, probability)),
            "elo_log_loss": float(log_loss(truth, elo)),
            "model_brier": float(brier_score_loss(truth, probability)),
            "elo_brier": float(brier_score_loss(truth, elo)),
            "model_accuracy": float(accuracy_score(truth, probability >= 0.5)),
            "model_auc": float(roc_auc_score(truth, probability)) if len(set(truth)) == 2 else None,
        }

    return {"protocol": "train 2000-2019; validation 2020-2022; test 2023-2025",
            "validation": metrics(validation), "test": metrics(test),
            "note": "Portfolio baseline; not the original R2 runtime artifact."}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(evaluate(args.data_dir), indent=2))


if __name__ == "__main__":
    main()
