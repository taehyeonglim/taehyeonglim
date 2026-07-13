import json
import os
import sys
import tempfile
import unittest
import xml.dom.minidom

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
import generate_activity as ga


def make_calendar(values):
    """values: 주간 합계 리스트 → 각 주를 7일로 쪼갠 GraphQL calendar 구조."""
    weeks = []
    day = 0
    for v in values:
        days = []
        base, rem = divmod(v, 7)
        for i in range(7):
            days.append({
                "date": f"2025-{(day // 28) % 12 + 1:02d}-{day % 28 + 1:02d}",
                "contributionCount": base + (1 if i < rem else 0),
            })
            day += 1
        weeks.append({"contributionDays": days})
    return {"totalContributions": sum(values), "weeks": weeks}


class WeeklySeriesTest(unittest.TestCase):
    def test_sums_days_per_week(self):
        cal = make_calendar([14, 0, 7])
        weeks, total = ga.weekly_series(cal)
        self.assertEqual([v for _, v in weeks], [14, 0, 7])
        self.assertEqual(total, 21)
        self.assertEqual(weeks[0][0], cal["weeks"][0]["contributionDays"][0]["date"])


class RenderSvgTest(unittest.TestCase):
    def setUp(self):
        self.values = [0, 3, 10, 42, 10, 3] + [5] * 46  # 52주, peak=42(index 3)
        cal = make_calendar(self.values)
        self.weeks, self.total = ga.weekly_series(cal)

    def test_valid_xml_both_palettes(self):
        for name in ("dark", "light"):
            svg = ga.render_svg(self.weeks, self.total, ga.PALETTES[name])
            xml.dom.minidom.parseString(svg)

    def test_bar_count_skips_zero_weeks(self):
        svg = ga.render_svg(self.weeks, self.total, ga.PALETTES["dark"])
        self.assertEqual(svg.count('class="bar"'), sum(1 for v in self.values if v > 0))

    def test_total_and_peak_annotations(self):
        svg = ga.render_svg(self.weeks, self.total, ga.PALETTES["dark"])
        self.assertIn(f"Σ {self.total:,} CONTRIBUTIONS / 365 DAYS", svg)
        self.assertIn("PEAK — 42/WK", svg)

    def test_palettes_differ(self):
        dark = ga.render_svg(self.weeks, self.total, ga.PALETTES["dark"])
        light = ga.render_svg(self.weeks, self.total, ga.PALETTES["light"])
        self.assertIn("#0d2a55", dark)
        self.assertIn("#f3f7fd", light)
        self.assertNotEqual(dark, light)

    def test_zero_data_renders_without_peak(self):
        cal = make_calendar([0] * 52)
        weeks, total = ga.weekly_series(cal)
        svg = ga.render_svg(weeks, total, ga.PALETTES["dark"])
        xml.dom.minidom.parseString(svg)
        self.assertNotIn("PEAK", svg)


class MainTest(unittest.TestCase):
    def test_fixture_mode_writes_two_files(self):
        cal = make_calendar([1] * 52)
        with tempfile.TemporaryDirectory() as td:
            fx = os.path.join(td, "cal.json")
            with open(fx, "w") as f:
                json.dump(cal, f)
            ga.main(["--user", "taehyeonglim", "--out", td, "--fixture", fx])
            for name in ("build-activity-dark.svg", "build-activity.svg"):
                path = os.path.join(td, name)
                self.assertTrue(os.path.exists(path), name)
                xml.dom.minidom.parse(path)


if __name__ == "__main__":
    unittest.main()
