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
SEG = (X1 - X0) // 5  # 88
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
    divs = "".join(
        f'<line x1="{X0 + SEG * i}" y1="17" x2="{X0 + SEG * i}" y2="29" stroke="{C["bg"]}" stroke-width="2"/>'
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
        f'<rect id="fill" x="{X0}" y="19" width="{SEG * phase}" height="8" fill="{fill}"/>'
        f"{divs}</svg>"
    )
