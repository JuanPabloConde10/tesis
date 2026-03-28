from copy import deepcopy
from typing import Any, Optional

from .judge_dimensions import DIMENSIONS

SUPPORTED_POLICIES = ("mean", "weighted")


def _validate_policies(policies: list[str]) -> list[str]:
    if not policies:
        return ["mean"]
    normalized = [p.strip().lower() for p in policies if p and p.strip()]
    if not normalized:
        return ["mean"]
    invalid = [p for p in normalized if p not in SUPPORTED_POLICIES]
    if invalid:
        raise ValueError(
            f"Unsupported policies: {invalid}. Supported: {list(SUPPORTED_POLICIES)}"
        )
    return normalized


def _normalize_weighted_weights(weights: dict[str, Any]) -> dict[str, float]:
    out: dict[str, float] = {}
    for dim in DIMENSIONS:
        if dim not in weights:
            raise ValueError(
                f"Missing weight for '{dim}' in weighted policy configuration"
            )
        try:
            out[dim] = float(weights[dim])
        except (TypeError, ValueError):
            raise ValueError(f"Invalid numeric weight for '{dim}': {weights[dim]}")

    total = sum(out.values())
    if total <= 0:
        raise ValueError("Weighted policy weights must sum to a positive value")

    return {dim: out[dim] / total for dim in DIMENSIONS}


def _extract_dimensions(candidate: dict[str, Any]) -> dict[str, Optional[float]]:
    if "evaluation" in candidate and isinstance(candidate["evaluation"], dict):
        dimensions = candidate["evaluation"].get("dimensions", {})
    else:
        dimensions = candidate.get("dimensions", {})

    out: dict[str, Optional[float]] = {}
    for dim in DIMENSIONS:
        value = dimensions.get(dim) if isinstance(dimensions, dict) else None
        try:
            out[dim] = float(value) if value is not None else None
        except (TypeError, ValueError):
            out[dim] = None
    return out


def _compute_mean_score(dimensions: dict[str, Optional[float]]) -> Optional[float]:
    vals = [v for v in dimensions.values() if v is not None]
    if not vals:
        return None
    return round(sum(vals) / len(vals), 4)


def _compute_weighted_score(
    dimensions: dict[str, Optional[float]],
    weights: dict[str, float],
) -> Optional[float]:
    numerator = 0.0
    denominator = 0.0
    for dim in DIMENSIONS:
        value = dimensions.get(dim)
        if value is None:
            continue
        weight = weights[dim]
        numerator += value * weight
        denominator += weight
    if denominator == 0:
        return None
    return round(numerator / denominator, 4)


def rank_candidates(
    candidates: list[dict[str, Any]],
    policies: Optional[list[str]] = None,
    weighted_policy_weights: Optional[dict[str, Any]] = None,
) -> dict[str, Any]:
    if not candidates:
        raise ValueError("No candidates provided for ranking")

    normalized_policies = _validate_policies(policies or [])
    normalized_weights: Optional[dict[str, float]] = None

    if "weighted" in normalized_policies:
        if weighted_policy_weights is None:
            raise ValueError(
                "Weighted policy selected but weighted_policy_weights is missing"
            )
        normalized_weights = _normalize_weighted_weights(weighted_policy_weights)

    rankings: dict[str, list[dict[str, Any]]] = {}
    winners: dict[str, dict[str, Any]] = {}

    for policy in normalized_policies:
        entries: list[dict[str, Any]] = []
        for candidate in candidates:
            dimensions = _extract_dimensions(candidate)
            if policy == "mean":
                score = _compute_mean_score(dimensions)
            else:
                score = _compute_weighted_score(dimensions, normalized_weights or {})

            entry = {
                "candidate_id": candidate.get("candidate_id"),
                "score": score,
                "dimensions": dimensions,
            }
            entries.append(entry)

        entries.sort(key=lambda item: item["score"] if item["score"] is not None else -1.0, reverse=True)
        rankings[policy] = entries

        top = entries[0]
        winner = next(
            (c for c in candidates if c.get("candidate_id") == top.get("candidate_id")),
            None,
        )
        if winner is None:
            raise RuntimeError("Unable to locate winner candidate after ranking")
        winner_payload = deepcopy(winner)
        winner_payload["policy"] = policy
        winner_payload["policy_score"] = top["score"]
        winners[policy] = winner_payload

    return {
        "policies": normalized_policies,
        "weighted_policy_weights_normalized": normalized_weights,
        "rankings": rankings,
        "winners": winners,
    }
