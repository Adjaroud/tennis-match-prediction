"""Explicit tennis-first candidate rules for the 13 official styles."""

from __future__ import annotations

import numpy as np

from .style_taxonomy import OFFICIAL_STYLE_ORDER


def m(row: dict, key: str, default: float = 50.0) -> float:
    """Read a numeric metric with a safe default."""
    value = row.get(key, default)
    if value is None:
        return default
    try:
        if np.isnan(value):
            return default
    except TypeError:
        pass
    return float(value)


def is_candidate_all_court_elite(row: dict) -> bool:
    return (
        m(row, "elo") >= 94
        and m(row, "surface_elo_mean") >= 86
        and m(row, "serve") >= 82
        and m(row, "ret_games") >= 78
        and m(row, "return_proxy") >= 80
        and m(row, "elite_surface_count", 0) >= 2
        and m(row, "career") >= 82
        and m(row, "matches", 0) >= 150
        and m(row, "grass_elo") >= 62
        and m(row, "one_surface_dependency") <= 16
        and m(row, "clay_dependency") <= 14
    )


def score_all_court_elite(row: dict) -> float:
    return 0.42 * m(row, "elo") + 0.18 * m(row, "surface_elo_mean") + 0.16 * m(row, "serve") + 0.18 * m(row, "return_proxy") + 0.06 * m(row, "balance")


def is_candidate_big_server(row: dict) -> bool:
    return m(row, "ace") >= 88 and m(row, "serve") >= 82 and m(row, "service_games_pct") >= 82 and m(row, "return_proxy") <= 58 and m(row, "ret_games") <= 58


def score_big_server(row: dict) -> float:
    return 0.42 * m(row, "ace") + 0.42 * m(row, "serve") + 0.16 * max(0, 65 - m(row, "ret_games"))


def is_candidate_big_server_baseliner(row: dict) -> bool:
    return m(row, "serve") >= 72 and m(row, "ace") >= 70 and 45 <= m(row, "return_proxy") <= 74 and max(m(row, "rally_proxy"), m(row, "attack_proxy")) >= 55 and m(row, "fast_score") >= 55


def score_big_server_baseliner(row: dict) -> float:
    return 0.36 * m(row, "serve") + 0.28 * m(row, "ace") + 0.16 * m(row, "return_proxy") + 0.12 * max(m(row, "rally_proxy"), m(row, "attack_proxy")) + 0.08 * m(row, "fast_score")


def is_candidate_power_baseliner(row: dict) -> bool:
    ground_evidence = max(m(row, "forehand"), m(row, "backhand"), m(row, "short_attack"), m(row, "external_attack")) >= 68
    service_driven_only = m(row, "ace") >= 88 and m(row, "return_proxy") < 55
    return ground_evidence and m(row, "attack_proxy") >= 68 and m(row, "return_proxy") >= 42 and m(row, "rally_proxy") >= 45 and not service_driven_only and not is_candidate_all_court_elite(row)


def score_power_baseliner(row: dict) -> float:
    return 0.46 * m(row, "attack_proxy") + 0.20 * max(m(row, "forehand"), m(row, "backhand"), m(row, "external_attack")) + 0.14 * m(row, "serve") + 0.12 * m(row, "return_proxy") + 0.08 * m(row, "elo")


def is_candidate_offensive_counterpuncher(row: dict) -> bool:
    return m(row, "return_proxy") >= 68 and m(row, "rally_proxy") >= 58 and m(row, "serve") <= 84 and m(row, "attack_proxy") >= 48 and not is_candidate_big_server(row)


def score_offensive_counterpuncher(row: dict) -> float:
    return 0.42 * m(row, "return_proxy") + 0.26 * m(row, "rally_proxy") + 0.16 * m(row, "ret_games") + 0.10 * m(row, "elo") + 0.06 * m(row, "attack_proxy")


def is_candidate_clay_specialist(row: dict) -> bool:
    return (
        (m(row, "clay") >= 55 or m(row, "clay_score") >= 68)
        and (m(row, "clay_elo") >= 55 or m(row, "clay_score") >= 68)
        and (m(row, "clay_dependency") >= 4 or m(row, "clay_dominant_identity", 0) >= 1)
        and m(row, "rally_proxy") >= 48
        and m(row, "clay_matches", 0) >= 15
        and m(row, "fast_score") <= m(row, "clay_score") + 28
        and not is_candidate_big_server(row)
    )


def score_clay_specialist(row: dict) -> float:
    return 0.34 * m(row, "clay_score") + 0.24 * max(0, m(row, "clay_dependency")) + 0.22 * m(row, "clay_elo") + 0.20 * m(row, "rally_proxy") + 18


def is_candidate_solid_offensive_server(row: dict) -> bool:
    return m(row, "serve") >= 62 and m(row, "ace") >= 45 and 35 <= m(row, "return_proxy") <= 72 and m(row, "variance_proxy") <= 82 and not is_candidate_big_server(row)


def score_solid_offensive_server(row: dict) -> float:
    return 0.42 * m(row, "serve") + 0.22 * m(row, "first") + 0.16 * m(row, "second") + 0.12 * m(row, "elo") + 0.08 * m(row, "balance")


def is_candidate_solid_offensive_returner(row: dict) -> bool:
    return m(row, "return_proxy") >= 62 and m(row, "ret_games") >= 60 and m(row, "serve") <= 82 and not (m(row, "rally_proxy") >= 72 and m(row, "return_proxy") >= 72)


def score_solid_offensive_returner(row: dict) -> float:
    return 0.46 * m(row, "return_proxy") + 0.24 * m(row, "ret_games") + 0.14 * m(row, "balance") + 0.10 * m(row, "elo") + 0.06 * m(row, "attack_proxy")


def is_candidate_topspin_baseliner(row: dict) -> bool:
    return (
        m(row, "rally_proxy") >= 60
        and max(m(row, "long_rally"), m(row, "rally_proxy")) >= 60
        and (m(row, "clay_score") >= 55 or m(row, "slow_score") >= 55 or m(row, "clay_boost") >= 1)
        and not is_candidate_big_server(row)
        and m(row, "short_attack") < 88
    )


def score_topspin_baseliner(row: dict) -> float:
    return 0.48 * m(row, "rally_proxy") + 0.20 * m(row, "clay_score") + 0.18 * max(0, m(row, "clay_boost")) + 0.14 * m(row, "long_rally") + 15


def is_candidate_solid_defensive(row: dict) -> bool:
    return m(row, "rally_proxy") >= 65 and m(row, "return_proxy") >= 55 and m(row, "attack_proxy") <= 68 and m(row, "serve") <= 76 and m(row, "variance_proxy") <= 70


def score_solid_defensive(row: dict) -> float:
    return 0.38 * m(row, "rally_proxy") + 0.28 * m(row, "return_proxy") + 0.22 * m(row, "balance") + 0.12 * max(0, 75 - m(row, "attack_proxy"))


def is_candidate_erratic_attacker(row: dict) -> bool:
    return m(row, "attack_proxy") >= 68 and m(row, "variance_proxy") >= 72 and not is_candidate_big_server(row) and not (m(row, "balance") >= 72 and m(row, "variance_proxy") < 78)


def score_erratic_attacker(row: dict) -> float:
    return 0.40 * m(row, "attack_proxy") + 0.32 * m(row, "variance_proxy") + 0.16 * m(row, "ace") + 0.12 * max(0, 70 - m(row, "ret_points"))


def is_candidate_serve_and_volley(row: dict) -> bool:
    return m(row, "external_weight", 0) >= 0.35 and m(row, "net_rush") >= 80 and m(row, "net_strength") >= 65 and m(row, "serve_volley") >= 75 and m(row, "serve") >= 65


def score_serve_and_volley(row: dict) -> float:
    return 0.46 * m(row, "net_proxy") + 0.22 * m(row, "serve_volley") + 0.18 * m(row, "serve") + 0.14 * m(row, "grass_elo")


def is_candidate_solid_offensive_core(row: dict) -> bool:
    no_extreme = not (
        is_candidate_all_court_elite(row)
        or is_candidate_big_server(row)
        or is_candidate_clay_specialist(row)
        or is_candidate_topspin_baseliner(row)
        or is_candidate_serve_and_volley(row)
    )
    return m(row, "serve") >= 45 and m(row, "return_proxy") >= 45 and m(row, "balance") >= 55 and m(row, "elo") >= 45 and no_extreme


def score_solid_offensive_core(row: dict) -> float:
    return 0.42 * m(row, "balance") + 0.20 * m(row, "elo") + 0.18 * m(row, "serve") + 0.18 * m(row, "return_proxy") + 0.02 * m(row, "career")


def redistribute_solid_core(row: dict, primary_style: str, secondary_style: str, candidate_scores: dict[str, float]) -> dict:
    """Redistribute SOLID_OFFENSIVE_CORE when a more precise tactical signal exists."""
    if primary_style != "SOLID_OFFENSIVE_CORE":
        return {
            "primary": primary_style,
            "secondary": secondary_style,
            "reason": "",
            "confidence": 0.0,
            "fallback_reason": "",
            "is_fallback_style": 0,
            "scores": candidate_scores,
        }
    serve = m(row, "serve")
    ret = m(row, "return_proxy")
    rally = m(row, "rally_proxy")
    attack = m(row, "attack_proxy")
    ace = m(row, "ace")
    clay_score = m(row, "clay_score")
    clay_identity = m(row, "clay_dominant_identity", 0)
    def result(style: str, secondary: str, reason: str, confidence: float) -> dict:
        scores = dict(candidate_scores)
        if scores.get(style, 0) <= 0 and style in STYLE_RULES:
            scores[style] = STYLE_RULES[style][1](row)
        return {
            "primary": style,
            "secondary": secondary,
            "reason": reason,
            "confidence": confidence,
            "fallback_reason": f"redistributed_from_solid_core:{reason}",
            "is_fallback_style": 0,
            "scores": scores,
        }
    if clay_score >= 78 and clay_identity >= 1:
        return result("CLAY_SPECIALIST", "TOPSPIN_BASELINER", "clay_identity_strong", 0.82)
    if clay_score >= 70 and rally >= 65:
        return result("TOPSPIN_BASELINER", "CLAY_SPECIALIST", "clay_rally_signal", 0.76)
    if clay_score >= 62 and rally >= 55 and serve < 82:
        return result("TOPSPIN_BASELINER", "CLAY_SPECIALIST", "moderate_clay_rally_signal", 0.66)
    if ret >= 75 and rally >= 70 and serve < 85:
        return result("OFFENSIVE_COUNTERPUNCHER", "SOLID_OFFENSIVE_RETURNER", "return_plus_rally_counter", 0.78)
    if ret >= 68 and rally >= 65 and serve < 85:
        return result("OFFENSIVE_COUNTERPUNCHER", "SOLID_OFFENSIVE_RETURNER", "moderate_return_rally_counter", 0.68)
    if ret >= 75 and rally < 70:
        return result("SOLID_OFFENSIVE_RETURNER", "OFFENSIVE_COUNTERPUNCHER", "return_leaning_core", 0.72)
    if ret >= 62 and serve <= 75 and (ret - serve >= 8 or m(row, "ret_games") >= 58):
        return result("SOLID_OFFENSIVE_RETURNER", "OFFENSIVE_COUNTERPUNCHER", "moderate_return_leaning_core", 0.66)
    if ret >= 50 and ret - serve >= 10:
        return result("SOLID_OFFENSIVE_RETURNER", "OFFENSIVE_COUNTERPUNCHER", "relative_return_leaning_core", 0.61)
    if rally >= 75 and attack < 60 and serve < 75:
        return result("SOLID_DEFENSIVE", "OFFENSIVE_COUNTERPUNCHER", "defensive_rally_core", 0.72)
    if rally >= 65 and attack < 55 and serve < 75 and ret >= 50:
        return result("SOLID_DEFENSIVE", "OFFENSIVE_COUNTERPUNCHER", "moderate_defensive_rally_core", 0.66)
    if serve >= 85 and attack >= 75 and ret >= 55:
        if ace >= 70:
            return result("BIG_SERVER_BASELINER", "SOLID_OFFENSIVE_SERVER", "serve_plus_baseline_attack", 0.75)
        return result("SOLID_OFFENSIVE_SERVER", "BIG_SERVER_BASELINER", "service_leaning_core", 0.70)
    if serve >= 70 and attack >= 65 and ret >= 45:
        if ace >= 60:
            return result("BIG_SERVER_BASELINER", "SOLID_OFFENSIVE_SERVER", "moderate_serve_baseline_attack", 0.67)
        return result("SOLID_OFFENSIVE_SERVER", "BIG_SERVER_BASELINER", "moderate_service_attack_core", 0.65)
    if serve >= 80 and ret < 70:
        return result("SOLID_OFFENSIVE_SERVER", "BIG_SERVER_BASELINER", "serve_leaning_core", 0.70)
    if serve >= 62 and ret < 55 and m(row, "first") >= 55:
        return result("SOLID_OFFENSIVE_SERVER", "BIG_SERVER_BASELINER", "moderate_serve_leaning_core", 0.65)
    if serve >= 50 and serve - ret >= 10:
        return result("SOLID_OFFENSIVE_SERVER", "BIG_SERVER_BASELINER", "relative_serve_leaning_core", 0.61)
    if attack >= 78 and ret >= 55 and serve >= 55:
        return result("POWER_BASELINER", "ERRATIC_ATTACKER", "power_core", 0.70)
    if attack >= 65 and ret >= 45 and serve >= 45 and rally >= 45:
        return result("POWER_BASELINER", "ERRATIC_ATTACKER", "moderate_power_core", 0.65)
    if attack >= 55 and attack - rally >= 8 and serve >= 40 and ret >= 25:
        return result("POWER_BASELINER", "ERRATIC_ATTACKER", "relative_power_core", 0.61)
    if attack >= 68 and serve >= 55 and ret < 45:
        return result("ERRATIC_ATTACKER", "POWER_BASELINER", "attack_with_return_gap", 0.64)
    true_balanced = serve >= 55 and ret >= 55 and attack >= 50 and rally >= 50 and m(row, "elo") >= 55 and max(abs(serve - ret), abs(attack - rally)) < 18
    fallback_reason = "true_balanced_core" if true_balanced else "balanced_no_strong_signal"
    return {
        "primary": "SOLID_OFFENSIVE_CORE",
        "secondary": secondary_style,
        "reason": "kept_core",
        "confidence": 0.55,
        "fallback_reason": fallback_reason,
        "is_fallback_style": int(fallback_reason == "balanced_no_strong_signal"),
        "scores": candidate_scores,
    }


STYLE_RULES = {
    "ALL_COURT_ELITE": (is_candidate_all_court_elite, score_all_court_elite),
    "BIG_SERVER_BASELINER": (is_candidate_big_server_baseliner, score_big_server_baseliner),
    "POWER_BASELINER": (is_candidate_power_baseliner, score_power_baseliner),
    "OFFENSIVE_COUNTERPUNCHER": (is_candidate_offensive_counterpuncher, score_offensive_counterpuncher),
    "CLAY_SPECIALIST": (is_candidate_clay_specialist, score_clay_specialist),
    "SOLID_OFFENSIVE_SERVER": (is_candidate_solid_offensive_server, score_solid_offensive_server),
    "SOLID_OFFENSIVE_RETURNER": (is_candidate_solid_offensive_returner, score_solid_offensive_returner),
    "SOLID_OFFENSIVE_CORE": (is_candidate_solid_offensive_core, score_solid_offensive_core),
    "BIG_SERVER": (is_candidate_big_server, score_big_server),
    "TOPSPIN_BASELINER": (is_candidate_topspin_baseliner, score_topspin_baseliner),
    "ERRATIC_ATTACKER": (is_candidate_erratic_attacker, score_erratic_attacker),
    "SOLID_DEFENSIVE": (is_candidate_solid_defensive, score_solid_defensive),
    "SERVE_AND_VOLLEY": (is_candidate_serve_and_volley, score_serve_and_volley),
}

DEFAULT_SECONDARY = {
    "ALL_COURT_ELITE": "OFFENSIVE_COUNTERPUNCHER",
    "BIG_SERVER_BASELINER": "SOLID_OFFENSIVE_SERVER",
    "POWER_BASELINER": "ERRATIC_ATTACKER",
    "OFFENSIVE_COUNTERPUNCHER": "SOLID_OFFENSIVE_RETURNER",
    "CLAY_SPECIALIST": "TOPSPIN_BASELINER",
    "SOLID_OFFENSIVE_SERVER": "BIG_SERVER_BASELINER",
    "SOLID_OFFENSIVE_RETURNER": "OFFENSIVE_COUNTERPUNCHER",
    "SOLID_OFFENSIVE_CORE": "SOLID_OFFENSIVE_SERVER",
    "BIG_SERVER": "SOLID_OFFENSIVE_SERVER",
    "TOPSPIN_BASELINER": "CLAY_SPECIALIST",
    "ERRATIC_ATTACKER": "POWER_BASELINER",
    "SOLID_DEFENSIVE": "OFFENSIVE_COUNTERPUNCHER",
    "SERVE_AND_VOLLEY": "BIG_SERVER",
}


def rank_style_candidates(row: dict) -> dict:
    """Return candidate scores, primary, secondary and fallback flag."""
    scores = {style: 0.0 for style in OFFICIAL_STYLE_ORDER}
    candidate_reasons = {}
    for style, (is_candidate, score_fn) in STYLE_RULES.items():
        if is_candidate(row):
            scores[style] = float(score_fn(row))
            candidate_reasons[style] = "candidate_rules_passed"
    is_fallback = False
    if not candidate_reasons:
        scores["SOLID_OFFENSIVE_CORE"] = max(35.0, score_solid_offensive_core(row))
        candidate_reasons["SOLID_OFFENSIVE_CORE"] = "balanced fallback"
        is_fallback = True
    ordered = sorted(candidate_reasons, key=lambda style: scores[style], reverse=True)
    primary = ordered[0]
    secondary = ordered[1] if len(ordered) > 1 else DEFAULT_SECONDARY.get(primary, "SOLID_OFFENSIVE_CORE")
    redistribution = redistribute_solid_core(row, primary, secondary, scores)
    primary = redistribution["primary"]
    secondary = redistribution["secondary"]
    scores = redistribution["scores"]
    return {
        "scores": scores,
        "candidate_reasons": candidate_reasons,
        "primary": primary,
        "secondary": secondary,
        "is_fallback_style": int(redistribution["is_fallback_style"] if primary == "SOLID_OFFENSIVE_CORE" else 0),
        "triggered_rule": redistribution["fallback_reason"] if str(redistribution["fallback_reason"]).startswith("redistributed_from_solid_core") else candidate_reasons.get(primary, redistribution["reason"] or "candidate_rules_passed"),
        "fallback_reason": redistribution["fallback_reason"] if primary == "SOLID_OFFENSIVE_CORE" else "",
        "redistribution_reason": redistribution["reason"],
        "redistribution_confidence": redistribution["confidence"],
    }
