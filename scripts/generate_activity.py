#!/usr/bin/env python3
"""FIG.04 — blueprint-style weekly contribution bar chart (dark/light SVG pair).

GitHub GraphQL contributionCalendar를 주간 합계로 접어 도면 스타일 막대 차트를 그린다.
표준 라이브러리만 사용. --fixture 로 오프라인 렌더 가능.
"""
import argparse
import json
import os
import sys
import urllib.request

GRAPHQL_URL = "https://api.github.com/graphql"
QUERY = (
    "query($login:String!){user(login:$login){contributionsCollection"
    "{contributionCalendar{totalContributions weeks{contributionDays"
    "{date contributionCount}}}}}}"
)

PALETTES = {
    "dark": {
        "bg0": "#0d2a55", "bg1": "#123a75", "grid": "#ffffff",
        "grid_fine": ".04", "grid_bold": ".07", "ink": "#dbeafe",
        "strong": "#eaf2ff", "mid": "#b9d0f0", "dim": "#8fb0dd",
        "red": "#f87171", "frame_op": ".6", "scan_op": ".16",
    },
    "light": {
        "bg0": "#ffffff", "bg1": "#f3f7fd", "grid": "#1e40af",
        "grid_fine": ".06", "grid_bold": ".09", "ink": "#1e40af",
        "strong": "#17337a", "mid": "#2c4d99", "dim": "#6981b8",
        "red": "#dc2626", "frame_op": ".55", "scan_op": ".12",
    },
}

MONTHS = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN",
          "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]

W, H = 1200, 340
X0, X1 = 70, 1140
Y_TOP, Y_BASE = 90, 272


def fetch_calendar(login, token):
    body = json.dumps({"query": QUERY, "variables": {"login": login}}).encode()
    req = urllib.request.Request(GRAPHQL_URL, data=body, headers={
        "Authorization": "bearer " + token,
        "Content-Type": "application/json",
        "User-Agent": "blueprint-activity",
    })
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.load(resp)
    if data.get("errors"):
        raise RuntimeError("GraphQL errors: %s" % data["errors"])
    return data["data"]["user"]["contributionsCollection"]["contributionCalendar"]


def weekly_series(calendar):
    weeks = []
    for wk in calendar["weeks"]:
        days = wk["contributionDays"]
        weeks.append((days[0]["date"], sum(d["contributionCount"] for d in days)))
    return weeks, calendar["totalContributions"]


def render_svg(weeks, total, p):
    n = max(len(weeks), 1)
    slot = (X1 - X0) / n
    bar_w = min(13.0, slot * 0.65)
    mx = max((v for _, v in weeks), default=0)
    scale = (Y_BASE - Y_TOP) / (mx if mx > 0 else 1)

    parts = []
    add = parts.append
    add('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" '
        'viewBox="0 0 %d %d" role="img" aria-labelledby="title desc">' % (W, H, W, H))
    add('<title id="title">Build activity — weekly contributions</title>')
    add('<desc id="desc">Blueprint-style bar chart of weekly GitHub contributions '
        'over the last year. FIG.04 of 4.</desc>')
    add('<defs>'
        '<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">'
        '<stop offset="0" stop-color="%(bg0)s"/><stop offset="1" stop-color="%(bg1)s"/>'
        '</linearGradient>'
        '<pattern id="gridFine" width="8" height="8" patternUnits="userSpaceOnUse">'
        '<path d="M8 0H0V8" fill="none" stroke="%(grid)s" stroke-opacity="%(grid_fine)s"/></pattern>'
        '<pattern id="gridBold" width="40" height="40" patternUnits="userSpaceOnUse">'
        '<path d="M40 0H0V40" fill="none" stroke="%(grid)s" stroke-opacity="%(grid_bold)s"/></pattern>'
        '<style>text{font-family:ui-monospace,\'SF Mono\',SFMono-Regular,Menlo,Consolas,'
        '\'Liberation Mono\',monospace;}'
        '.scan{animation:scan 16s linear infinite;}'
        '@keyframes scan{to{transform:translateX(1180px);}}'
        '@media (prefers-reduced-motion:reduce){.scan{animation:none;}}'
        '</style></defs>' % p)
    add('<rect width="%d" height="%d" fill="url(#bg)"/>' % (W, H))
    add('<rect width="%d" height="%d" fill="url(#gridFine)"/>' % (W, H))
    add('<rect width="%d" height="%d" fill="url(#gridBold)"/>' % (W, H))
    add('<rect x="2" y="2" width="%d" height="%d" fill="none" stroke="%s" '
        'stroke-opacity="%s" stroke-width="2.5"/>' % (W - 4, H - 4, p["ink"], p["frame_op"]))
    add('<rect x="10" y="10" width="%d" height="%d" fill="none" stroke="%s" '
        'stroke-opacity=".28"/>' % (W - 20, H - 20, p["ink"]))
    add('<g stroke="%s" stroke-opacity=".3" stroke-width="6" stroke-dasharray="1 39">'
        '<line x1="10" y1="13" x2="1190" y2="13"/>'
        '<line x1="10" y1="%d" x2="1190" y2="%d"/>'
        '<line x1="13" y1="10" x2="13" y2="%d"/>'
        '<line x1="1187" y1="10" x2="1187" y2="%d"/></g>'
        % (p["ink"], H - 13, H - 13, H - 10, H - 10))
    add('<rect class="scan" x="10" y="10" width="1" height="%d" fill="%s" '
        'fill-opacity="%s"/>' % (H - 20, p["ink"], p["scan_op"]))
    add('<text x="54" y="54" font-size="14" font-weight="700" letter-spacing="3" '
        'fill="%s">BUILD ACTIVITY</text>' % p["mid"])
    add('<text x="1146" y="54" text-anchor="end" font-size="12" font-weight="700" '
        'letter-spacing="1" fill="%s">Σ %s CONTRIBUTIONS / 365 DAYS</text>'
        % (p["strong"], format(total, ",")))
    add('<text x="1170" y="32" text-anchor="end" font-size="9.5" letter-spacing="2" '
        'fill="%s">SHEET 04 / 04</text>' % p["dim"])

    # y축 눈금선 + 라벨
    for val, y in ((mx, Y_TOP), (mx // 2, (Y_TOP + Y_BASE) // 2), (0, Y_BASE)):
        if y != Y_BASE:
            add('<path d="M%d %dH%d" stroke="%s" stroke-opacity=".18" '
                'stroke-dasharray="3 6" fill="none"/>' % (X0, y, X1, p["ink"]))
        add('<text x="%d" y="%d" text-anchor="end" font-size="9" fill="%s">%d</text>'
            % (X0 - 8, y + 3, p["dim"], val))
    add('<path d="M%d %dH%d" stroke="%s" stroke-opacity=".6" fill="none"/>'
        % (X0 - 4, Y_BASE, X1 + 4, p["ink"]))

    # 막대 + 월 라벨
    peak_i = -1
    if mx > 0:
        peak_i = max(range(len(weeks)), key=lambda i: weeks[i][1])
    prev_month = None
    for i, (dstr, v) in enumerate(weeks):
        bx = X0 + i * slot + (slot - bar_w) / 2
        month = int(dstr[5:7])
        if month != prev_month:
            if prev_month is not None:
                add('<text x="%.1f" y="%d" font-size="9.5" letter-spacing="1" '
                    'fill="%s">%s</text>' % (bx, Y_BASE + 18, p["dim"], MONTHS[month - 1]))
                add('<path d="M%.1f %dv5" stroke="%s" stroke-opacity=".5" fill="none"/>'
                    % (bx, Y_BASE, p["ink"]))
            prev_month = month
        if v <= 0:
            continue
        h = max(v * scale, 2.0)
        color = p["red"] if i == peak_i else p["ink"]
        fill_op = ".75" if i == peak_i else ".5"
        add('<rect class="bar" x="%.1f" y="%.1f" width="%.1f" height="%.1f" '
            'fill="%s" fill-opacity="%s" stroke="%s" stroke-opacity=".9"/>'
            % (bx, Y_BASE - h, bar_w, h, color, fill_op, color))

    # 피크 콜아웃
    if peak_i >= 0 and weeks[peak_i][1] > 0:
        v = weeks[peak_i][1]
        px = X0 + peak_i * slot + slot / 2
        py = Y_BASE - max(v * scale, 2.0)
        if px <= 980:
            add('<path d="M%.1f %.1fv-16h40" stroke="%s" stroke-opacity=".9" fill="none"/>'
                % (px, py - 4, p["red"]))
            add('<text x="%.1f" y="%.1f" font-size="10.5" font-weight="800" '
                'letter-spacing="1" fill="%s">PEAK — %d/WK</text>'
                % (px + 46, py - 16, p["red"], v))
        else:
            add('<path d="M%.1f %.1fv-16h-40" stroke="%s" stroke-opacity=".9" fill="none"/>'
                % (px, py - 4, p["red"]))
            add('<text x="%.1f" y="%.1f" text-anchor="end" font-size="10.5" '
                'font-weight="800" letter-spacing="1" fill="%s">PEAK — %d/WK</text>'
                % (px - 46, py - 16, p["red"], v))

    # 타이틀 블록
    add('<g font-size="8.5">'
        '<rect x="884" y="%d" width="306" height="24" fill="none" stroke="%s" '
        'stroke-opacity=".5"/>'
        '<path d="M946 %dv24M1086 %dv24M1144 %dv24" stroke="%s" stroke-opacity=".35"/>'
        '<text x="915" y="%d" text-anchor="middle" font-weight="800" letter-spacing="1" '
        'fill="%s">FIG.04</text>'
        '<text x="1016" y="%d" text-anchor="middle" fill="%s">DWG NO. TL-2026-04</text>'
        '<text x="1115" y="%d" text-anchor="middle" fill="%s">REV 2026.07</text>'
        '<text x="1167" y="%d" text-anchor="middle" fill="%s">SCALE 1:1</text></g>'
        % (H - 36, p["ink"], H - 36, H - 36, H - 36, p["ink"],
           H - 21, p["red"], H - 21, p["mid"], H - 21, p["mid"], H - 21, p["mid"]))
    add('</svg>')
    return "".join(parts)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--user", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--fixture", help="calendar JSON 경로 (오프라인 렌더)")
    args = ap.parse_args(argv)

    if args.fixture:
        with open(args.fixture) as f:
            calendar = json.load(f)
    else:
        token = os.environ.get("GITHUB_TOKEN")
        if not token:
            sys.exit("GITHUB_TOKEN 환경변수가 필요합니다 (또는 --fixture 사용).")
        calendar = fetch_calendar(args.user, token)

    weeks, total = weekly_series(calendar)
    os.makedirs(args.out, exist_ok=True)
    for palette, filename in (("dark", "build-activity-dark.svg"),
                              ("light", "build-activity.svg")):
        path = os.path.join(args.out, filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(render_svg(weeks, total, PALETTES[palette]))
        print("wrote", path)


if __name__ == "__main__":
    main()
