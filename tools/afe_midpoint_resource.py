"""Midpoint resource indexing and activation helpers from the attached AFE specification.

The loader does not fabricate the referenced 60+ axis dataset. It indexes whatever
resource JSON is supplied and reports missing or unavailable interpretations plainly.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, Mapping


@dataclass(frozen=True)
class MidpointActivation:
    activating_planet: str
    midpoint: str
    longitude: float
    orb: float
    interpretation: str
    evidence_class: str = "source_derived"

    def as_dict(self) -> dict:
        return self.__dict__.copy()


class MidpointResourceLoader:
    def __init__(self, json_path: str | Path | None = None, data: Mapping[str, Any] | None = None) -> None:
        self.json_path = str(json_path) if json_path is not None else None
        if data is not None:
            self.data = dict(data)
        elif json_path is not None and Path(json_path).exists():
            self.data = json.loads(Path(json_path).read_text(encoding="utf-8"))
        else:
            self.data = {}
        self.index: Dict[str, Dict[str, str]] = {}
        self._build_index()

    def _build_index(self) -> None:
        root = self.data.get("midpoints_resource", self.data)
        sections = root.get("sections", {}) if isinstance(root, Mapping) else {}
        if not isinstance(sections, Mapping):
            return

        for planet, section in sections.items():
            if not isinstance(section, Mapping):
                continue
            entries: list[Any] = []
            preferred_key = f"all_{str(planet).lower()}_midpoints"
            if isinstance(section.get(preferred_key), list):
                entries.extend(section[preferred_key])
            for key, value in section.items():
                if key == preferred_key:
                    continue
                if key in {"midpoints", "entries", "activations"} and isinstance(value, list):
                    entries.extend(value)
            planet_index = self.index.setdefault(str(planet), {})
            for entry in entries:
                if not isinstance(entry, Mapping):
                    continue
                axis = entry.get("axis") or entry.get("midpoint")
                interpretation = entry.get("interpretation")
                if isinstance(axis, str) and isinstance(interpretation, str) and interpretation.strip():
                    planet_index[axis] = interpretation.strip()

    def get_interpretation(self, activating_planet: str, midpoint_axis: str) -> str:
        return self.index.get(activating_planet, {}).get(midpoint_axis, "")

    def get_all_for_planet(self, activating_planet: str) -> Dict[str, str]:
        return dict(self.index.get(activating_planet, {}))

    def get_all_axes(self) -> list[str]:
        return sorted({axis for axes in self.index.values() for axis in axes})

    def get_activating_planets(self) -> list[str]:
        return sorted(self.index)

    def search(self, query: str) -> list[dict]:
        needle = query.casefold()
        return [
            {"planet": planet, "axis": axis, "interpretation": interpretation}
            for planet, axes in self.index.items()
            for axis, interpretation in axes.items()
            if needle in interpretation.casefold() or needle in axis.casefold() or needle in planet.casefold()
        ]

    def find_activations(
        self,
        midpoint_longitudes: Mapping[str, float],
        transit_positions: Mapping[str, float],
        orb: float = 1.0,
    ) -> list[dict]:
        if orb < 0:
            raise ValueError("orb must be non-negative")
        activations: list[dict] = []
        for midpoint, midpoint_longitude in midpoint_longitudes.items():
            for planet, longitude in transit_positions.items():
                distance = abs((float(longitude) - float(midpoint_longitude)) % 360)
                distance = min(distance, 360 - distance)
                interpretation = self.get_interpretation(str(planet), str(midpoint))
                if distance <= orb and interpretation:
                    activations.append(MidpointActivation(str(planet), str(midpoint), float(midpoint_longitude) % 360, distance, interpretation).as_dict())
        return activations
