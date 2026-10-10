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


ROOT = os.path.join(os.path.dirname(__file__), "..")
IMG = ('<img src="https://raw.githubusercontent.com/taehyeonglim/taehyeonglim/output/progress/'
       '{repo}.svg" width="460" alt="{repo} progress">')
ITEM_RE = re.compile(
    r"^- \*\*(?:\[[^\]]+\]\(https://github\.com/taehyeonglim/(?P<linked>[A-Za-z0-9._-]+)\)"
    r"|(?P<private>[A-Za-z0-9._-]+)\*\* \(private\))"
)


def readme_items():
    with open(os.path.join(ROOT, "README.md"), encoding="utf-8") as f:
        lines = f.read().split("\n")
    items = []
    for i, line in enumerate(lines):
        m = ITEM_RE.match(line)
        if m:
            items.append((m.group("linked") or m.group("private"), line,
                          lines[i + 1] if i + 1 < len(lines) else ""))
    return items


class ReadmeSyncTest(unittest.TestCase):
    def setUp(self):
        with open(os.path.join(ROOT, "data", "progress.json"), encoding="utf-8") as f:
            self.data = json.load(f)

    def test_data_is_valid(self):
        gp.validate(self.data)

    def test_readme_repos_match_data(self):
        repos = [r for r, _, _ in readme_items()]
        self.assertEqual(len(repos), len(set(repos)))
        self.assertEqual(set(repos), set(self.data))

    def test_each_item_has_its_gauge_below(self):
        for repo, line, nxt in readme_items():
            self.assertTrue(line.endswith("<br>"), repo)
            self.assertEqual(nxt, "  " + IMG.format(repo=repo), repo)

    def test_parser_extracts_both_forms(self):
        m1 = ITEM_RE.match("- **[esports-landscape](https://github.com/taehyeonglim/2026-esports-landscape)** — x")
        m2 = ITEM_RE.match("- **Graduate-School-of-Education-AI-Agent** (private) — x")
        self.assertEqual(m1.group("linked"), "2026-esports-landscape")
        self.assertEqual(m2.group("private"), "Graduate-School-of-Education-AI-Agent")
