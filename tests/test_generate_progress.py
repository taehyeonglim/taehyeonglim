import json
import os
import re
import sys
import tempfile
import unittest
import xml.dom.minidom

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
import generate_progress as gp


def fill_width(svg):
    m = re.search(r'<rect id="fill" x="10" y="19" width="([\d.]+)"', svg)
    return float(m.group(1))


class RenderTest(unittest.TestCase):
    def test_fill_width_tracks_phase(self):
        for p in range(1, 6):
            self.assertEqual(fill_width(gp.render_gauge("x", p, "active")), 88 * p)

    def test_readout_text(self):
        svg = gp.render_gauge("NERV", 4, "active")
        self.assertIn("04/05 :: OPERATIONAL", svg)
        self.assertIn("■ ACTIVE", svg)

    def test_active_fill_orange_complete_green(self):
        self.assertIn('fill="#ff6a00"', gp.render_gauge("x", 3, "active").split('id="fill"')[1][:80])
        self.assertIn('fill="#3dff9a"', gp.render_gauge("x", 5, "active").split('id="fill"')[1][:80])

    def test_standby_uses_hazard(self):
        svg = gp.render_gauge("learning-agent", 2, "standby")
        self.assertIn("▲ STANDBY", svg)
        self.assertIn('fill="url(#hz-learning-agent)"', svg)

    def test_title_and_valid_xml_for_odd_names(self):
        for name in ["2026-esports-landscape", "a.b_c", "NERV"]:
            svg = gp.render_gauge(name, 1, "standby")
            xml.dom.minidom.parseString(svg)
            self.assertIn(f"<title>{name} — SYS.PHASE 01/05 DESIGN · STANDBY</title>", svg)


class ValidateTest(unittest.TestCase):
    def test_accepts_valid(self):
        gp.validate({"NERV": {"phase": 4, "status": "active"}})

    def test_rejects_bad_values(self):
        bad = [
            [],
            {"NERV": 4},
            {"NERV": {"phase": 0, "status": "active"}},
            {"NERV": {"phase": 6, "status": "active"}},
            {"NERV": {"phase": "3", "status": "active"}},
            {"NERV": {"phase": True, "status": "active"}},
            {"NERV": {"phase": 3, "status": "paused"}},
            {"NERV": {"phase": 3, "status": "active", "pct": 50}},
            {"../x": {"phase": 3, "status": "active"}},
        ]
        for d in bad:
            with self.assertRaises(ValueError, msg=repr(d)):
                gp.validate(d)


class CliTest(unittest.TestCase):
    def test_writes_one_svg_per_repo_into_new_dir(self):
        with tempfile.TemporaryDirectory() as d:
            data = os.path.join(d, "p.json")
            with open(data, "w") as f:
                json.dump({"NERV": {"phase": 4, "status": "active"},
                           "ww2": {"phase": 5, "status": "active"}}, f)
            out = os.path.join(d, "nested", "progress")
            self.assertEqual(gp.main(["--data", data, "--out", out]), 0)
            self.assertEqual(sorted(os.listdir(out)), ["NERV.svg", "ww2.svg"])

    def test_invalid_data_returns_1(self):
        with tempfile.TemporaryDirectory() as d:
            data = os.path.join(d, "p.json")
            with open(data, "w") as f:
                json.dump({"NERV": {"phase": 9, "status": "active"}}, f)
            self.assertEqual(gp.main(["--data", data, "--out", d]), 1)

    def test_malformed_json_returns_1(self):
        with tempfile.TemporaryDirectory() as d:
            data = os.path.join(d, "p.json")
            with open(data, "w") as f:
                f.write("{not json")
            self.assertEqual(gp.main(["--data", data, "--out", d]), 1)
