"""Transit strength and house affinity utilities from the attached AFE specification.

The speed table is source-derived placeholder metadata until real ephemeris speeds
are supplied. Results are methodology-bound and should not be treated as forecasts.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Mapping


class DignityLevel(int, Enum):
    DOMICILE = 5
    EXALTATION = 4
    TRIPLICITY = 3
    TERM = 2
    FACE = 1
    PEREGRINE = 0
    DETRIMENT = -4
    FALL = -5


class AvashtaState(str, Enum):
    JAGRAD = "awake"
    SVAPNA = "sleepy"
    SUSHUPTI = "asleep"


class HouseAffinityEngine:
    def __init__(self) -> None:
        self.affinities = {
            "Sun": {"strong": [1, 5, 10], "weak": [4, 6, 7, 8, 12]},
            "Moon": {"strong": [2, 4], "weak": [6, 8, 10, 12]},
            "Mercury": {"strong": [1, 3], "weak": [7, 8, 12]},
            "Venus": {"strong": [2, 4, 7], "weak": [6, 8, 10]},
            "Mars": {"strong": [1, 10], "weak": [4, 6, 12]},
            "Jupiter": {"strong": [1, 4, 9], "weak": [6, 7, 8]},
            "Saturn": {"strong": [7, 10, 11], "weak": [1, 4]},
        }

    def get_affinity_bonus(self, planet: str, house: int) -> float:
        data = self.affinities.get(planet)
        if data is None:
            return 1.0
        if house in data["strong"]:
            return 1.5
        if house in data["weak"]:
            return 0.5
        return 1.0

    def get_interpretation(self, planet: str, house: int) -> str:
        data = self.affinities.get(planet)
        if data is None:
            return "Neutral house placement."
        if house in data["strong"]:
            return "Strong house affinity."
        if house in data["weak"]:
            return "Weak house affinity."
        return "Neutral house placement."


@dataclass(frozen=True)
class TransitStrengthResult:
    transit_planet: str
    natal_planet: str
    aspect: str
    orb: float
    dignity_score: int
    final_dispositor: str
    dispositor_score: int
    speed_modifier: float
    house_modifier: float
    avashta: str
    avashta_modifier: float
    orb_modifier: float
    aspect_modifier: float
    strength: float
    active: bool
    evidence_class: str = "methodology_bound"

    def as_dict(self) -> dict:
        return self.__dict__.copy()


class TransitStrengthEngine:
    SIGNS = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
    RULERS = {
        "Aries": "Mars", "Taurus": "Venus", "Gemini": "Mercury", "Cancer": "Moon",
        "Leo": "Sun", "Virgo": "Mercury", "Libra": "Venus", "Scorpio": "Pluto",
        "Sagittarius": "Jupiter", "Capricorn": "Saturn", "Aquarius": "Saturn", "Pisces": "Jupiter",
    }
    EXALTATIONS = {"Aries": "Sun", "Taurus": "Moon", "Cancer": "Jupiter", "Virgo": "Mercury", "Libra": "Saturn", "Capricorn": "Mars", "Pisces": "Venus"}
    OPPOSITES = {"Aries": "Libra", "Taurus": "Scorpio", "Gemini": "Sagittarius", "Cancer": "Capricorn", "Leo": "Aquarius", "Virgo": "Pisces", "Libra": "Aries", "Scorpio": "Taurus", "Sagittarius": "Gemini", "Capricorn": "Cancer", "Aquarius": "Leo", "Pisces": "Virgo"}
    FALLS = {"Aries": "Saturn", "Taurus": "Mars", "Cancer": "Saturn", "Virgo": "Venus", "Libra": "Sun", "Capricorn": "Jupiter", "Pisces": "Mercury"}
    SPEEDS = {"Moon": 0.2, "Mercury": 0.5, "Venus": 0.6, "Mars": 0.8, "Sun": 0.7, "Jupiter": 1.2, "Saturn": 1.5, "Uranus": 2.0, "Neptune": 2.0, "Pluto": 2.0}
    ASPECT_ANGLES = {"conjunction": 0, "semi-sextile": 30, "semi-square": 45, "sextile": 60, "quintile": 72, "square": 90, "trine": 120, "sesquiquadrate": 135, "biquintile": 144, "quincunx": 150, "opposition": 180}

    def __init__(self, natal_positions: Mapping[str, float], transit_positions: Mapping[str, float], ascendant: float, house_cusps: Mapping[int, float] | None = None) -> None:
        self.natal = {k: float(v) % 360 for k, v in natal_positions.items()}
        self.transit = {k: float(v) % 360 for k, v in transit_positions.items()}
        self.ascendant = float(ascendant) % 360
        self.house_cusps = {int(k): float(v) % 360 for k, v in (house_cusps or {}).items()}
        self.affinity = HouseAffinityEngine()

    def get_sign(self, longitude: float) -> str:
        return self.SIGNS[int(float(longitude) % 360 // 30) % 12]

    def get_house(self, longitude: float) -> int:
        if not self.house_cusps:
            return 1
        cusps = sorted(self.house_cusps.items())
        value = float(longitude) % 360
        for index, (house, cusp) in enumerate(cusps):
            next_cusp = cusps[(index + 1) % len(cusps)][1]
            if index == len(cusps) - 1 or cusp > next_cusp:
                inside = value >= cusp or value < next_cusp
            else:
                inside = cusp <= value < next_cusp
            if inside:
                return house
        return 1

    def get_essential_dignity_score(self, planet: str, longitude: float) -> int:
        sign = self.get_sign(longitude)
        if self.RULERS.get(sign) == planet:
            return DignityLevel.DOMICILE.value
        if self.EXALTATIONS.get(sign) == planet:
            return DignityLevel.EXALTATION.value
        elements = {
            "Fire": {"Aries", "Leo", "Sagittarius"}, "Earth": {"Taurus", "Virgo", "Capricorn"},
            "Air": {"Gemini", "Libra", "Aquarius"}, "Water": {"Cancer", "Scorpio", "Pisces"},
        }
        natal_sign = self.get_sign(self.natal.get(planet, 0.0))
        if any(sign in group and natal_sign in group for group in elements.values()):
            return DignityLevel.TRIPLICITY.value
        if self.OPPOSITES.get(sign) == planet:
            return DignityLevel.DETRIMENT.value
        if self.FALLS.get(sign) == planet:
            return DignityLevel.FALL.value
        return DignityLevel.PEREGRINE.value

    def get_dispositor_chain(self, planet: str) -> List[str]:
        chain = [planet]
        visited = set()
        current = planet
        while current not in visited:
            visited.add(current)
            ruler = self.RULERS.get(self.get_sign(self.natal.get(current, 0.0)))
            if not ruler or ruler == current or ruler not in self.natal:
                break
            chain.append(ruler)
            current = ruler
        return chain

    def get_final_dispositor(self, planet: str) -> str:
        return self.get_dispositor_chain(planet)[-1]

    def get_speed_modifier(self, planet: str) -> float:
        return self.SPEEDS.get(planet, 1.0)

    def get_house_modifier(self, longitude: float) -> float:
        house = self.get_house(longitude)
        return 1.5 if house in (1, 4, 7, 10) else 1.0 if house in (2, 5, 8, 11) else 0.6

    def get_avashta_state(self, planet: str, longitude: float) -> AvashtaState:
        score = self.get_essential_dignity_score(planet, longitude)
        return AvashtaState.JAGRAD if score >= 3 else AvashtaState.SVAPNA if score >= 0 else AvashtaState.SUSHUPTI

    @staticmethod
    def get_avashta_modifier(state: AvashtaState) -> float:
        return {AvashtaState.JAGRAD: 1.5, AvashtaState.SVAPNA: 1.0, AvashtaState.SUSHUPTI: 0.5}[state]

    @staticmethod
    def get_orb_modifier(orb: float) -> float:
        return 2.0 if orb <= 1 else 1.5 if orb <= 2 else 1.0 if orb <= 3 else 0.5

    def get_aspect_type(self, angle: float) -> str:
        angle = float(angle) % 360
        angle = min(angle, 360 - angle)
        matches = [(abs(angle - target), name) for name, target in self.ASPECT_ANGLES.items() if abs(angle - target) <= 2]
        return min(matches)[1] if matches else "unknown"

    @staticmethod
    def get_aspect_modifier(aspect_type: str) -> float:
        return 1.2 if aspect_type in {"conjunction", "trine", "sextile"} else 0.8 if aspect_type in {"square", "opposition"} else 1.0

    def compute_transit_strength(self, transit_planet: str, natal_planet: str) -> dict:
        transit_longitude = self.transit.get(transit_planet, 0.0)
        natal_longitude = self.natal.get(natal_planet, 0.0)
        angle = abs((transit_longitude - natal_longitude) % 360)
        angle = min(angle, 360 - angle)
        aspect = self.get_aspect_type(angle)
        target_angle = self.ASPECT_ANGLES.get(aspect, 0)
        orb = abs(angle - target_angle)
        dignity = self.get_essential_dignity_score(transit_planet, transit_longitude)
        final_dispositor = self.get_final_dispositor(transit_planet)
        dispositor_score = self.get_essential_dignity_score(final_dispositor, self.natal.get(final_dispositor, 0.0))
        state = self.get_avashta_state(transit_planet, transit_longitude)
        strength = (dignity + dispositor_score) * self.get_speed_modifier(transit_planet) * self.get_house_modifier(transit_longitude) * self.get_avashta_modifier(state) * self.get_orb_modifier(orb) * self.get_aspect_modifier(aspect)
        return TransitStrengthResult(transit_planet, natal_planet, aspect, orb, dignity, final_dispositor, dispositor_score, self.get_speed_modifier(transit_planet), self.get_house_modifier(transit_longitude), state.value, self.get_avashta_modifier(state), self.get_orb_modifier(orb), self.get_aspect_modifier(aspect), strength, orb <= 8).as_dict()

    def compute_all_transits(self) -> List[dict]:
        return [result for transit in self.transit for natal in self.natal if (result := self.compute_transit_strength(transit, natal))["active"]]
