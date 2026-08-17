"""Canonical, provenance-aware delineation ontology helpers.

This module normalizes record shape only. It does not calculate astronomical
positions or assert interpretive truth.
"""
from __future__ import annotations

from typing import Any, Iterable

EVIDENCE_CLASSES = {
    "source_derived",
    "normalized",
    "computed",
    "methodology_bound",
    "research_exploratory",
    "synthesized",
    "pending_review",
    "unavailable",
    "not_implemented",
}


def _unique(values: Iterable[str] | None) -> list[str]:
    return list(dict.fromkeys(str(v) for v in (values or []) if v is not None and str(v)))


def normalize_observation(
    *,
    observation_id: str,
    point: str,
    source_ids: Iterable[str],
    status: str = "source_derived",
    calculated_value: Any = None,
    settings: dict[str, Any] | None = None,
    extensions: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if not observation_id or not point:
        raise ValueError("observation_id and point are required")
    if status not in EVIDENCE_CLASSES:
        raise ValueError(f"unsupported evidence status: {status}")
    return {
        "observation_id": observation_id,
        "point": point,
        "source_ids": _unique(source_ids),
        "status": status,
        "calculated_value": calculated_value,
        "settings": settings or {},
        "extensions": extensions or {},
    }


def build_interpretation(
    *,
    interpretation_id: str,
    tradition: str,
    statement: str,
    evidence_refs: Iterable[str],
    source_ids: Iterable[str],
    status: str = "source_derived",
    limitations: Iterable[str] | None = None,
) -> dict[str, Any]:
    if not interpretation_id or not tradition or not statement:
        raise ValueError("interpretation_id, tradition, and statement are required")
    if status not in EVIDENCE_CLASSES:
        raise ValueError(f"unsupported evidence status: {status}")
    return {
        "interpretation_id": interpretation_id,
        "tradition": tradition,
        "statement": statement,
        "evidence_refs": _unique(evidence_refs),
        "source_ids": _unique(source_ids),
        "status": status,
        "limitations": _unique(limitations),
    }


def build_formula_reference(
    *,
    formula_id: str,
    formula: str,
    source_ids: Iterable[str],
    status: str = "pending_review",
    required_inputs: Iterable[str] | None = None,
    outputs: Iterable[str] | None = None,
    failure_mode: str = "unavailable_with_recommendation",
) -> dict[str, Any]:
    if not formula_id or not formula:
        raise ValueError("formula_id and formula are required")
    return {
        "formula_id": formula_id,
        "formula": formula,
        "source_ids": _unique(source_ids),
        "status": status,
        "required_inputs": _unique(required_inputs),
        "outputs": _unique(outputs),
        "failure_mode": failure_mode,
    }


def validate_chart_methodology(methodology: dict[str, Any]) -> list[str]:
    required = ("chart_type", "status", "inputs", "outputs", "source_ids", "limitations")
    errors = [f"missing:{key}" for key in required if key not in methodology]
    if methodology.get("status") not in {"contracted", "source_derived", "pending_review", "not_implemented", "unavailable"}:
        errors.append("invalid:status")
    if not isinstance(methodology.get("inputs", []), list):
        errors.append("invalid:inputs")
    if not isinstance(methodology.get("outputs", []), list):
        errors.append("invalid:outputs")
    if not isinstance(methodology.get("source_ids", []), list):
        errors.append("invalid:source_ids")
    return errors
