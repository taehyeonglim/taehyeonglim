# Project Progress Gauge Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** README Open source(18)·Private(21) 각 항목 아래에 `data/progress.json`에서 생성한 NERV "MAGI 터미널 리드아웃" 진행 게이지 SVG를 붙인다.

**Architecture:** 표준 라이브러리 Python 스크립트(`scripts/generate_progress.py`)가 JSON을 검증하고 레포별 460×34 SVG를 그린다. 기존 `blueprint-activity.yml` build job이 이를 `dist/progress/`에 생성해 `output` 브랜치로 배포하고, README는 raw URL로 참조한다. 동기화 테스트가 README 항목·이미지와 데이터 키의 일치를 보장한다.

**Tech Stack:** Python 3 stdlib, unittest(pytest 러너), GitHub Actions.

**Spec:** `docs/superpowers/specs/2026-10-10-project-progress-gauge-design.md`

## Global Constraints

- phase ∈ {1,2,3,4,5} ↔ `DESIGN`,`BUILD`,`DEPLOYED`,`OPERATIONAL`,`COMPLETE`; status ∈ {`active`,`standby`}.
- 데이터 키 = GitHub 레포 이름, 정규식 `^[A-Za-z0-9._-]+$`. 데이터에 다른 필드 없음.
- SVG 460×34, 다크/라이트 공용 단일 파일, 경로 `progress/<repo>.svg`.
- 색: 배경 `#0a0c12`, 테두리 `#ff6a00` .35, 라벨 `#9a7048`, active 판독 `#ffb000`, standby 판독 `#5b6070`, ACTIVE 태그 `#3dff9a`, STANDBY 태그 `#ffb000`, 트랙 `#141826`, active 채움 `#ff6a00`, phase5 active 채움 `#3dff9a`, standby 채움 = 45° 해저드(`#ffb000` .55, 폭 4/주기 8).
- 바: x=10~450, y=19, 높이 8, 채움 폭 88·phase, 구분선 x=10+88·i (i=1..4).
- README 이미지: `<img src="https://raw.githubusercontent.com/taehyeonglim/taehyeonglim/output/progress/<repo>.svg" width="460" alt="<repo> progress">`, 항목 줄 끝 `<br>` + 다음 줄 2칸 들여쓰기.
- 표준 라이브러리만 사용.

## Review Focus

- 레포 이름이 숫자로 시작(`2026-esports-landscape`)하거나 `.`을 포함 → 패턴 id·파일명이 유효해야 함 (Task 1 테스트로 고정).
- 데이터 JSON이 객체가 아니거나 항목이 객체가 아님(`"NERV": 4`) → 명확한 `ValueError` (Task 1).
- phase가 `true`(bool은 int의 하위형) → 거부해야 함 (Task 1).
- README Private 항목 이름에 정규식 특수문자 포함 가능 → 동기화 파서가 링크/비링크 두 형식 모두 정확히 추출 (Task 3).
- 출력 디렉터리 미존재 → CLI가 생성 (Task 2).

---

### Task 1: 게이지 렌더러 + 데이터 검증

**Files:**
- Create: `scripts/generate_progress.py`
- Test: `tests/test_generate_progress.py`

**Interfaces:**
- Produces: `PHASES: list[str]`, `validate(data: object) -> None` (위반 시 `ValueError`), `render_gauge(repo: str, phase: int, status: str) -> str`

- [ ] **Step 1: 실패하는 테스트 작성** — `tests/test_generate_progress.py`

```python
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
```

- [ ] **Step 2: 실패 확인** — Run: `python3 -m pytest tests/test_generate_progress.py -q` → Expected: `ModuleNotFoundError: generate_progress`

- [ ] **Step 3: 최소 구현** — `scripts/generate_progress.py`

```python
#!/usr/bin/env python3
"""PROGRESS — NERV MAGI-terminal 진행 게이지 (레포별 460×34 SVG).

data/progress.json 의 {repo: {phase, status}} 를 검증하고 레포마다 게이지를 그린다.
다크/라이트 공용 단일 룩. 표준 라이브러리만 사용.
"""
import argparse
import json
import os
import re
import sys

PHASES = ["DESIGN", "BUILD", "DEPLOYED", "OPERATIONAL", "COMPLETE"]
STATUSES = ("active", "standby")
NAME_RE = re.compile(r"^[A-Za-z0-9._-]+$")

W, H = 460, 34
X0, X1 = 10, 450
SEG = (X1 - X0) / 5  # 88
MONO = "ui-monospace,'SF Mono',SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"
C = {
    "bg": "#0a0c12", "frame": "#ff6a00", "label": "#9a7048", "read": "#ffb000",
    "read_off": "#5b6070", "ok": "#3dff9a", "warn": "#ffb000", "track": "#141826",
    "fill": "#ff6a00", "done": "#3dff9a",
}


def validate(data):
    if not isinstance(data, dict):
        raise ValueError("progress data must be a JSON object")
    for repo, entry in data.items():
        if not NAME_RE.match(repo):
            raise ValueError(f"invalid repo name: {repo!r}")
        if not isinstance(entry, dict) or set(entry) != {"phase", "status"}:
            raise ValueError(f"{repo}: entry must be exactly {{phase, status}}")
        phase = entry["phase"]
        if isinstance(phase, bool) or not isinstance(phase, int) or not 1 <= phase <= 5:
            raise ValueError(f"{repo}: phase must be an integer 1-5")
        if entry["status"] not in STATUSES:
            raise ValueError(f"{repo}: status must be one of {STATUSES}")


def render_gauge(repo, phase, status):
    active = status == "active"
    code = PHASES[phase - 1]
    pid = f"hz-{repo}"
    if active:
        fill = C["done"] if phase == 5 else C["fill"]
    else:
        fill = f"url(#{pid})"
    tag, tag_c = ("■ ACTIVE", C["ok"]) if active else ("▲ STANDBY", C["warn"])
    width = SEG * phase
    width = int(width) if width == int(width) else width
    divs = "".join(
        f'<line x1="{X0 + SEG * i:g}" y1="17" x2="{X0 + SEG * i:g}" y2="29" stroke="{C["bg"]}" stroke-width="2"/>'
        for i in range(1, 5)
    )
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
        f'role="img" font-family="{MONO}">'
        f"<title>{repo} — SYS.PHASE 0{phase}/05 {code} · {status.upper()}</title>"
        f'<defs><pattern id="{pid}" width="8" height="8" patternUnits="userSpaceOnUse" '
        f'patternTransform="rotate(45)"><rect width="4" height="8" fill="{C["warn"]}" fill-opacity=".55"/></pattern></defs>'
        f'<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" fill="{C["bg"]}" stroke="{C["frame"]}" stroke-opacity=".35"/>'
        f'<text x="10" y="13" font-size="9" letter-spacing="2" fill="{C["label"]}">SYS.PHASE</text>'
        f'<text x="78" y="13" font-size="9" font-weight="800" letter-spacing="2" '
        f'fill="{C["read"] if active else C["read_off"]}">0{phase}/05 :: {code}</text>'
        f'<text x="{W - 10}" y="13" text-anchor="end" font-size="9" font-weight="800" letter-spacing="2" fill="{tag_c}">{tag}</text>'
        f'<rect x="{X0}" y="19" width="{X1 - X0}" height="8" fill="{C["track"]}"/>'
        f'<rect id="fill" x="{X0}" y="19" width="{width}" height="8" fill="{fill}"/>'
        f"{divs}</svg>"
    )
```

- [ ] **Step 4: 통과 확인** — Run: `python3 -m pytest tests/test_generate_progress.py -q` → Expected: 7 passed

- [ ] **Step 5: 커밋**

```bash
git add scripts/generate_progress.py tests/test_generate_progress.py
git commit -m "feat(progress): MAGI-terminal gauge renderer and data validation"
```

---

### Task 2: CLI + CI 단계

**Files:**
- Modify: `scripts/generate_progress.py` (끝에 `main` 추가)
- Modify: `.github/workflows/blueprint-activity.yml` (build job, "Generate activity SVGs" 다음)
- Test: `tests/test_generate_progress.py`

**Interfaces:**
- Consumes: `validate`, `render_gauge` (Task 1)
- Produces: `main(argv: list[str] | None = None) -> int` — `--data PATH --out DIR`, 성공 0, 검증 실패 시 stderr 메시지 + 1

- [ ] **Step 1: 실패하는 테스트 추가**

```python
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
```

- [ ] **Step 2: 실패 확인** — Run: `python3 -m pytest tests/test_generate_progress.py -q -k Cli` → Expected: `AttributeError: ... 'main'`

- [ ] **Step 3: 구현** — `scripts/generate_progress.py` 끝에 추가

```python
def main(argv=None):
    ap = argparse.ArgumentParser(description="Render NERV progress gauges")
    ap.add_argument("--data", default="data/progress.json")
    ap.add_argument("--out", default="dist/progress")
    args = ap.parse_args(argv)
    try:
        with open(args.data, encoding="utf-8") as f:
            data = json.load(f)
        validate(data)
    except (OSError, ValueError) as e:  # json.JSONDecodeError ⊂ ValueError
        print(f"generate_progress: {e}", file=sys.stderr)
        return 1
    os.makedirs(args.out, exist_ok=True)
    for repo, entry in data.items():
        with open(os.path.join(args.out, f"{repo}.svg"), "w", encoding="utf-8") as f:
            f.write(render_gauge(repo, entry["phase"], entry["status"]))
    print(f"wrote {len(data)} gauges to {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 4: CI 단계 추가** — `.github/workflows/blueprint-activity.yml`의 "Generate activity SVGs" 스텝 바로 다음:

```yaml
      - name: Generate progress gauges
        run: python3 scripts/generate_progress.py --data data/progress.json --out dist/progress
```

- [ ] **Step 5: 통과 확인** — Run: `python3 -m pytest -q` → Expected: 전체 통과

- [ ] **Step 6: 커밋**

```bash
git add scripts/generate_progress.py tests/test_generate_progress.py .github/workflows/blueprint-activity.yml
git commit -m "feat(progress): CLI and CI step rendering gauges to output branch"
```

---

### Task 3: 초기 데이터 + README 게이지 + 동기화 테스트

**Files:**
- Create: `data/progress.json` (39 항목, 사용자 확정 표 기준)
- Modify: `README.md` (Open source 18 + Private 21 항목)
- Test: `tests/test_generate_progress.py`

**Interfaces:**
- Consumes: `validate` (Task 1)

- [ ] **Step 1: 초안 표 작성·사용자 확정** — 레포별 근거(homepage/라이브 URL, 최근 30일 커밋, README Phase 표기, 마지막 커밋일)를 수집해 `레포 | phase | status | 근거` 표로 제시하고 사용자 수정 반영. 확정 전 Step 3 이후 진행 금지.

- [ ] **Step 2: 실패하는 동기화 테스트 추가**

```python
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
```

- [ ] **Step 3: 실패 확인** — Run: `python3 -m pytest tests/test_generate_progress.py -q -k ReadmeSync` → Expected: FAIL (`data/progress.json` 없음)

- [ ] **Step 4: `data/progress.json` 작성** — 확정 표의 39 항목을 `{"<repo>": {"phase": N, "status": "active|standby"}}` 형식으로, README 등장 순서대로, 2칸 들여쓰기.

- [ ] **Step 5: README 수정** — 스크립트로 각 항목 줄 끝에 `<br>`, 다음 줄에 `"  " + IMG.format(repo=...)` 삽입 (항목 줄 판별은 `ITEM_RE`와 동일 정규식).

- [ ] **Step 6: 통과 + 렌더 확인** — Run: `python3 -m pytest -q` → 전체 통과. `python3 scripts/generate_progress.py --out <scratch>/progress` 후 headless Chrome으로 샘플 3장(active/standby/complete) 렌더 육안 확인. GitHub markdown API(`gh api markdown`)로 README Open source·Private 블록 렌더 시 `<img` 39개 확인.

- [ ] **Step 7: 커밋 (push는 사용자 확인 후)**

```bash
git add data/progress.json README.md tests/test_generate_progress.py
git commit -m "feat(readme): progress gauge under each Open source and Private entry"
```

- [ ] **Step 8: push 후 검증** — push → Actions build 성공 확인(`gh run watch`) → `curl -sI https://raw.githubusercontent.com/taehyeonglim/taehyeonglim/output/progress/NERV.svg` 200 확인.
