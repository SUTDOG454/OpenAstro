"""Arabic Parts/Lots engine derived from the attached AFE specification.

This module implements only formulas explicitly present in the preserved source.
It is a symbolic calculation utility, not an empirical or financial predictor.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Dict, Mapping, Tuple


class ChartSect(str, Enum):
    DIURNAL = "diurnal"
    NOCTURNAL = "nocturnal"


@dataclass(frozen=True)
class ArabicPartResult:
    name: str
    longitude: float
    sign_index: int
    house: int
    interpretation: str

    def as_dict(self) -> dict:
        return {
            "name": self.name,
            "longitude": self.longitude,
            "sign": self.sign_index,
            "house": self.house,
            "interpretation": self.interpretation,
            "evidence_class": "computed",
            "method": "afe-arabic-parts-v7-source-derived",
        }


class ArabicPartsEngine:
    """Calculate the explicitly specified Arabic Parts for a chart."""

    def __init__(
        self,
        positions: Mapping[str, float],
        ascendant: float,
        house_cusps: Mapping[int, float] | None = None,
        sun_above_horizon: bool = True,
    ) -> None:
        self.positions = {str(k): float(v) % 360 for k, v in positions.items()}
        self.ascendant = float(ascendant) % 360
        self.house_cusps = {int(k): float(v) % 360 for k, v in (house_cusps or {}).items()}
        self.sect = ChartSect.DIURNAL if sun_above_horizon else ChartSect.NOCTURNAL

    @staticmethod
    def normalize_longitude(value: float) -> float:
        return float(value) % 360

    @staticmethod
    def measure_arc(point_a: float, point_b: float) -> float:
        return (float(point_b) - float(point_a)) % 360

    def get_position(self, point: str) -> float:
        if point == "Ascendant":
            return self.ascendant
        if point.startswith("House_"):
            try:
                return self.house_cusps.get(int(point.split("_", 1)[1]), 0.0)
            except (IndexError, ValueError):
                return 0.0
        if point.startswith("Sign_"):
            try:
                return (int(point.split("_", 1)[1]) * 30) % 360
            except (IndexError, ValueError):
                return 0.0
        return self.positions.get(point, 0.0)

    def calculate_part(self, significator_a: str, significator_b: str, projection: str = "Ascendant") -> float:
        return self.normalize_longitude(
            self.get_position(projection)
            + self.measure_arc(self.get_position(significator_a), self.get_position(significator_b))
        )

    def _sign_and_house(self, longitude: float) -> Tuple[int, int]:
        sign = int(self.normalize_longitude(longitude) // 30) % 12
        if not self.house_cusps:
            return sign, 1
        cusps = sorted(self.house_cusps.items())
        for index, (house, cusp) in enumerate(cusps):
            next_cusp = cusps[(index + 1) % len(cusps)][1]
            if index == len(cusps) - 1:
                in_arc = longitude >= cusp or longitude < next_cusp
            elif cusp <= next_cusp:
                in_arc = cusp <= longitude < next_cusp
            else:
                in_arc = longitude >= cusp or longitude < next_cusp
            if in_arc:
                return sign, house
        return sign, 1

    def _result(self, name: str, longitude: float, interpretation: str) -> ArabicPartResult:
        sign, house = self._sign_and_house(longitude)
        return ArabicPartResult(name, longitude, sign, house, interpretation)

    def part_of_fortune(self) -> ArabicPartResult:
        longitude = self.calculate_part("Sun", "Moon") if self.sect == ChartSect.DIURNAL else self.calculate_part("Moon", "Sun")
        return self._result("Part of Fortune", longitude, "Life, body, soul, wealth, reputation, all things")

    def part_of_future(self) -> ArabicPartResult:
        longitude = self.calculate_part("Moon", "Sun") if self.sect == ChartSect.DIURNAL else self.calculate_part("Sun", "Moon")
        return self._result("Part of Future", longitude, "Soul, faith, prophecy, hidden things, intentions")

    def part_of_saturn(self) -> ArabicPartResult:
        fortune = self.part_of_fortune().longitude
        longitude = self.normalize_longitude(
            self.ascendant + ((fortune - self.get_position("Saturn")) if self.sect == ChartSect.DIURNAL else (self.get_position("Saturn") - fortune))
        )
        return self._result("Part of Saturn", longitude, "Memory, profundity, loss, death, inheritance")

    def part_of_life(self) -> ArabicPartResult:
        longitude = self.calculate_part("Jupiter", "Saturn") if self.sect == ChartSect.DIURNAL else self.calculate_part("Saturn", "Jupiter")
        return self._result("Part of Life", longitude, "Natural life, body, sustenance, longevity")

    def part_of_father(self) -> ArabicPartResult:
        saturn = self.get_position("Saturn")
        sun = self.get_position("Sun")
        separation = min(abs(saturn - sun), 360 - abs(saturn - sun))
        first, second = ("Jupiter", "Sun") if separation < 8 and self.sect == ChartSect.DIURNAL else ("Sun", "Jupiter") if separation < 8 else ("Sun", "Saturn") if self.sect == ChartSect.DIURNAL else ("Saturn", "Sun")
        longitude = self.calculate_part(first, second)
        return self._result("Part of Father", longitude, "Father's fortune, substance, origin")

    def part_of_mother(self) -> ArabicPartResult:
        longitude = self.calculate_part("Venus", "Moon") if self.sect == ChartSect.DIURNAL else self.calculate_part("Moon", "Venus")
        return self._result("Part of Mother", longitude, "Mother's being, love between mother and child")

    def part_of_marriage(self) -> ArabicPartResult:
        return self._result("Part of Marriage", self.calculate_part("Saturn", "Venus"), "Long-lasting marriage, marriage quality and fortune")

    def part_of_death(self) -> ArabicPartResult:
        moon = self.get_position("Moon")
        eighth = self.get_position("House_8")
        saturn = self.get_position("Saturn")
        saturn_sign = int(saturn // 30) % 12
        saturn_degree = saturn - saturn_sign * 30
        longitude = self.normalize_longitude(saturn_sign * 30 + self.measure_arc(moon, eighth) + saturn_degree)
        return self._result("Part of Death", longitude, "Manner and quality of death")

    def part_of_kingship(self) -> ArabicPartResult:
        longitude = self.calculate_part("Mars", "Moon") if self.sect == ChartSect.DIURNAL else self.calculate_part("Moon", "Mars")
        return self._result("Part of Kingship", longitude, "Attainment of rule, authority, connection to the powerful")

    def part_of_grain(self) -> ArabicPartResult:
        return self._result("Part of Grain", self.calculate_part("Sun", "Mars"), "Price and abundance of grain")

    def compute_all_parts(self) -> Dict[str, dict]:
        results = [
            self.part_of_fortune(), self.part_of_future(), self.part_of_saturn(), self.part_of_life(),
            self.part_of_father(), self.part_of_mother(), self.part_of_marriage(), self.part_of_death(),
            self.part_of_kingship(), self.part_of_grain(),
        ]
        return {result.name: result.as_dict() for result in results}
