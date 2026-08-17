import hashlib
import json
import unittest
from pathlib import Path

from tools.afe_arabic_parts import ArabicPartsEngine, ChartSect
from tools.afe_midpoint_resource import MidpointResourceLoader
from tools.afe_transit_strength import AvashtaState, HouseAffinityEngine, TransitStrengthEngine

ROOT = Path(__file__).resolve().parents[1]


class ArabicPartsTests(unittest.TestCase):
    def setUp(self):
        self.positions = {
            "Sun": 10,
            "Moon": 40,
            "Saturn": 70,
            "Jupiter": 100,
            "Venus": 130,
            "Mars": 160,
        }
        self.cusps = {house: (house - 1) * 30 for house in range(1, 13)}

    def test_diurnal_and_nocturnal_fortune_reverse_formula(self):
        day = ArabicPartsEngine(self.positions, 100, self.cusps, sun_above_horizon=True)
        night = ArabicPartsEngine(self.positions, 100, self.cusps, sun_above_horizon=False)
        self.assertEqual(day.sect, ChartSect.DIURNAL)
        self.assertEqual(day.part_of_fortune().longitude, 130.0)
        self.assertEqual(night.part_of_fortune().longitude, 70.0)

    def test_all_parts_are_normalized_and_provenanced(self):
        result = ArabicPartsEngine(self.positions, 100, self.cusps).compute_all_parts()
        self.assertEqual(len(result), 10)
        self.assertTrue(all(0 <= item["longitude"] < 360 for item in result.values()))
        self.assertTrue(all(item["evidence_class"] == "computed" for item in result.values()))

    def test_missing_house_cusp_is_safe(self):
        engine = ArabicPartsEngine(self.positions, 100, {})
        self.assertEqual(engine.part_of_death().house, 1)


class MidpointResourceTests(unittest.TestCase):
    def setUp(self):
        self.loader = MidpointResourceLoader(data={
            "midpoints_resource": {
                "sections": {
                    "Jupiter": {"all_jupiter_midpoints": [{"axis": "Sun/Moon", "interpretation": "growth"}]},
                    "Saturn": {"all_saturn_midpoints": [{"axis": "Venus/Mars", "interpretation": "constraint"}]},
                }
            }
        })

    def test_index_and_search(self):
        self.assertEqual(self.loader.get_interpretation("Jupiter", "Sun/Moon"), "growth")
        self.assertEqual(self.loader.get_all_axes(), ["Sun/Moon", "Venus/Mars"])
        self.assertEqual(self.loader.get_activating_planets(), ["Jupiter", "Saturn"])
        self.assertEqual(self.loader.search("GROWTH")[0]["planet"], "Jupiter")
        self.assertEqual(self.loader.get_interpretation("Neptune", "Sun/Moon"), "")

    def test_activation_uses_circular_orb_distance(self):
        activations = self.loader.find_activations({"Sun/Moon": 359.5}, {"Jupiter": 0.0}, orb=1.0)
        self.assertEqual(len(activations), 1)
        self.assertAlmostEqual(activations[0]["orb"], 0.5)
        self.assertEqual(activations[0]["evidence_class"], "source_derived")

    def test_negative_orb_is_rejected(self):
        with self.assertRaises(ValueError):
            self.loader.find_activations({}, {}, orb=-1)


class TransitStrengthTests(unittest.TestCase):
    def setUp(self):
        self.engine = TransitStrengthEngine(
            natal_positions={"Sun": 0, "Moon": 10, "Mars": 180},
            transit_positions={"Sun": 10},
            ascendant=0,
            house_cusps={house: (house - 1) * 30 for house in range(1, 13)},
        )

    def test_dignity_aspect_and_avashta_contracts(self):
        self.assertEqual(self.engine.get_sign(0), "Aries")
        self.assertEqual(self.engine.get_essential_dignity_score("Sun", 0), 4)
        self.assertEqual(self.engine.get_aspect_type(359), "conjunction")
        self.assertEqual(self.engine.get_avashta_state("Sun", 0), AvashtaState.JAGRAD)

    def test_transit_strength_is_active_for_exact_conjunction(self):
        result = self.engine.compute_transit_strength("Sun", "Moon")
        self.assertEqual(result["aspect"], "conjunction")
        self.assertAlmostEqual(result["orb"], 0.0)
        self.assertTrue(result["active"])
        self.assertEqual(result["evidence_class"], "methodology_bound")

    def test_house_affinity_defaults(self):
        affinity = HouseAffinityEngine()
        self.assertEqual(affinity.get_affinity_bonus("Sun", 1), 1.5)
        self.assertEqual(affinity.get_affinity_bonus("Sun", 6), 0.5)
        self.assertEqual(affinity.get_affinity_bonus("Unknown", 3), 1.0)


class AttachmentProvenanceTests(unittest.TestCase):
    def test_all_four_attachments_are_preserved_and_midpoint_files_are_duplicate(self):
        raw = ROOT / "data" / "extractions" / "afe-unified" / "raw"
        files = sorted(raw.glob("*.txt"))
        self.assertEqual(len(files), 4)
        hashes = {path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in files}
        self.assertEqual(hashes["afe-midpoint-resource-v7-a.txt"], hashes["afe-midpoint-resource-v7-b.txt"])
        self.assertGreater(len(json.loads((ROOT / "data" / "resources" / "midpoints_resource.sample.json").read_text())["midpoints_resource"]["sections"]), 0)


if __name__ == "__main__":
    unittest.main()
