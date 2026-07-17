# NERV 프로필 리스킨 구현 계획

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** GitHub 프로필의 SVG 자산 8쌍을 블루프린트 테마에서 NERV 테마(다크=MAGI 터미널, 라이트=NERV 공문서)로 인플레이스 리스킨한다.

**Architecture:** 파일명·README 마크업·output 브랜치 불변. 정적 SVG 7쌍은 손조판(다크 먼저, 라이트는 동일 지오메트리에 팔레트·장치 치환), FIG.05는 `generate_activity.py`의 PALETTES·템플릿 교체. 디스플레이 타이포는 `scripts/textpath.py`(신규)로 Chakra Petch를 패스 아웃라인으로 변환해 임베드.

**Tech Stack:** 손조판 SVG, Python 3 (stdlib + fontTools), 헤드리스 Chrome 검증, GitHub Actions(불변).

**스펙:** `docs/superpowers/specs/2026-07-17-nerv-profile-reskin-design.md` (동일 레포)

## Global Constraints

- **작업 디렉토리**: `/Users/taehyeong/Documents/GitHub/taehyeonglim` (main 브랜치). 모든 경로는 여기 기준.
- **스크래치**: `$SCRATCH` = `/private/tmp/claude-501/-Users-taehyeong-Documents-GitHub-cv/a8eda218-dad1-4cbe-ad9f-5bbbb5c5efa9/scratchpad` (스크린샷·폰트 저장, 레포에 커밋 금지).
- **다크 팔레트 (MAGI 터미널)**: 바탕 `#050609→#0a0c12` + 상단 레드 radial `rgba(217,39,32,.11)` / 잉크 제목 `#f4efe6` 본문 `#d8d5ce` muted `#8d9098` dim `#5c6069` / 레드 `#ff3b30`(밝음) `#d92720`(기본) `#780f10`(딥) / 앰버 `#ffb000`(FIG.05·상태 전용) / 그린 `#34d399`(텔레메트리 전용) / 그리드 `#f4efe6` 8px op `.03` + 40px op `.05` + 레드 축선 `rgba(255,59,48,.16)`.
- **라이트 팔레트 (NERV 공문서)**: 종이 `#f4efe6` + 음영 `#ece5d8` / 먹 제목 `#1a1b1e` 본문 `#2a2b30` muted `#6b6558` / 레드 `#d92720` / 괘선 `#1a1b1e` op `.08`~`.12`. **먹+레드 2색 원칙 — 앰버·그린 금지.**
- **모션**: 다크만 스캔라인 1개 + blink, `prefers-reduced-motion: reduce` 대응 필수. **라이트는 `animation` 문자열 자체가 없어야 한다.** 버튼 3종은 양 모드 모두 정적.
- **타이포**: 라벨·본문 `ui-monospace,'SF Mono',SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace`. 디스플레이(히어로 메인, FIG.03 타이틀)만 Chakra Petch SemiBold 패스 아웃라인. 변환 품질 미달 시 시스템 모노 대문자 + 자간으로 폴백.
- **일본어는 히어로 서브라벨 `協働知能システム` 1곳만.** 다른 자산 금지.
- **원작 NERV 반잎 로고 등 원작 도형 사용 금지.**
- **콘텐츠 보존**: 각 태스크의 "보존 문구" 목록이 전부 결과물에 존재해야 한다 (grep 검증). `SHEET NN / 05` 연번 유지.
- **문서 헤더 (구 타이틀 블록)**: 4칸 — `FIG.NN` / `DOC NO. NERV-TL-2026-NN` / `REV 2026.07` / `MAGI CHECKED`. `DWG NO.`·`SCALE 1:1`은 폐기.
- **viewBox 불변**: hero 1200×320, research-map 1200×440, project-nerv 1200×270, field-results 1200×200, 버튼 148/172×34, activity 1200×340.
- **외부 리소스 0**: `href="http…"` 등 외부 참조 금지 (xmlns 선언 제외). 전 SVG `<title>`+`<desc>` 갱신(NERV 서술).
- **README.md·`.github/workflows/*` 수정 금지.**
- **커밋**: 태스크당 1커밋, 메시지 끝에 `Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>`. **push는 Task 8의 사용자 최종 승인 후에만.**
- **검증 공통 명령** (매 SVG): ① `xmllint --noout <파일>` ② 헤드리스 크롬 `"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless --disable-gpu --screenshot=$SCRATCH/<이름>.png --window-size=<W>,<H> "file://<절대경로>"` ③ 스크린샷 PNG를 Read 도구로 열어 육안 확인.

---

### Task 1: `scripts/textpath.py` — Chakra Petch 패스 변환 도구

**Files:**
- Create: `scripts/textpath.py`
- Create: `tests/test_textpath.py`
- 다운로드(비커밋): `$SCRATCH/ChakraPetch-SemiBold.ttf`

**Interfaces:**
- Produces: `text_to_path(font_path: str, text: str, size: float, tracking_em: float = 0.0) -> tuple[str, float]` — SVG path `d` 문자열(원점=베이스라인 좌측, y축 아래방향)과 전체 폭. CLI: `python3 scripts/textpath.py FONT.ttf "TEXT" SIZE [tracking_em]` → 1행 `<!-- width=NNN.N -->` + 2행 `d` 문자열. Task 2·5가 소비.

- [ ] **Step 1: 폰트 다운로드**

```bash
SCRATCH=/private/tmp/claude-501/-Users-taehyeong-Documents-GitHub-cv/a8eda218-dad1-4cbe-ad9f-5bbbb5c5efa9/scratchpad
curl -fL -o "$SCRATCH/ChakraPetch-SemiBold.ttf" \
  "https://raw.githubusercontent.com/google/fonts/main/ofl/chakrapetch/ChakraPetch-SemiBold.ttf"
ls -la "$SCRATCH/ChakraPetch-SemiBold.ttf"
```

Expected: 파일 존재, 크기 대략 90~250KB. 404면 같은 디렉토리의 `ChakraPetch-Bold.ttf`로 폴백(이하 경로 치환). Chakra Petch는 SIL OFL — 아웃라인 임베드 허용.

- [ ] **Step 2: 실패하는 테스트 작성** — `tests/test_textpath.py`

```python
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
from textpath import text_to_path

FONT = os.environ.get(
    "CHAKRA_TTF",
    "/private/tmp/claude-501/-Users-taehyeong-Documents-GitHub-cv/"
    "a8eda218-dad1-4cbe-ad9f-5bbbb5c5efa9/scratchpad/ChakraPetch-SemiBold.ttf",
)


@unittest.skipUnless(os.path.exists(FONT), "Chakra Petch TTF 없음 — plan Task 1 Step 1 참조")
class TextToPathTest(unittest.TestCase):
    def test_returns_path_and_advance(self):
        d, width = text_to_path(FONT, "AI", 100)
        self.assertTrue(d.startswith("M"))
        self.assertGreater(width, 50)

    def test_tracking_widens_advance(self):
        _, w0 = text_to_path(FONT, "AI", 100, 0.0)
        _, w1 = text_to_path(FONT, "AI", 100, 0.1)
        self.assertAlmostEqual(w1 - w0, 20.0, places=3)

    def test_missing_glyph_advances_half_em(self):
        _, w_sp = text_to_path(FONT, " ", 100)
        self.assertGreater(w_sp, 0)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 3: 실패 확인**

Run: `cd /Users/taehyeong/Documents/GitHub/taehyeonglim && python3 -m unittest tests.test_textpath -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'textpath'`

- [ ] **Step 4: 구현** — `scripts/textpath.py`

```python
#!/usr/bin/env python3
"""TTF 글리프를 SVG 패스 아웃라인으로 변환하는 조판 도구.

GitHub README의 <img> SVG는 외부 폰트를 로드할 수 없으므로, 대형
디스플레이 타이포(Chakra Petch)는 이 도구로 패스를 생성해 임베드한다.
사용: python3 scripts/textpath.py FONT.ttf "TEXT" SIZE [tracking_em]
출력: 1행 <!-- width=NNN.N -->, 2행 <path d="..."> 에 넣을 d 문자열.
원점은 베이스라인 좌측 (SVG 좌표계, y축 아래방향).
"""
import sys

from fontTools.misc.transform import Transform
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont


def text_to_path(font_path, text, size, tracking_em=0.0):
    font = TTFont(font_path)
    cmap = font.getBestCmap()
    glyphs = font.getGlyphSet()
    upm = font["head"].unitsPerEm
    scale = size / upm
    x = 0.0
    d = []
    for ch in text:
        name = cmap.get(ord(ch))
        if name is None:  # 글리프 없음 → 0.5em 전진
            x += size * 0.5 + tracking_em * size
            continue
        glyph = glyphs[name]
        pen = SVGPathPen(glyphs)
        glyph.draw(TransformPen(pen, Transform(scale, 0, 0, -scale, x, 0)))
        cmd = pen.getCommands()
        if cmd:
            d.append(cmd)
        x += glyph.width * scale + tracking_em * size
    return " ".join(d), x


def main():
    font_path, text, size = sys.argv[1], sys.argv[2], float(sys.argv[3])
    tracking = float(sys.argv[4]) if len(sys.argv) > 4 else 0.0
    d, width = text_to_path(font_path, text, size, tracking)
    print("<!-- width=%.1f -->" % width)
    print(d)


if __name__ == "__main__":
    main()
```

- [ ] **Step 5: 테스트 통과 확인**

Run: `python3 -m unittest tests.test_textpath -v`
Expected: `OK` (3 tests). 기존 스위트 회귀 확인: `python3 -m unittest discover -s tests -v` → 전부 PASS.

- [ ] **Step 6: 커밋**

```bash
git add scripts/textpath.py tests/test_textpath.py
git commit -m "feat(scripts): textpath — Chakra Petch outline tool

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 2: FIG.01 히어로 쌍 + 공통 스캐폴드 확립 → 시안 게이트

**Files:**
- Modify: `assets/hero-dark.svg` (전면 교체, viewBox `0 0 1200 320` 유지)
- Modify: `assets/hero-light.svg` (동일)

**Interfaces:**
- Consumes: Task 1 CLI — 예: `python3 scripts/textpath.py "$SCRATCH/ChakraPetch-SemiBold.ttf" "HUMAN × AI" 64 0.02`
- Produces: 이 태스크에서 확립한 defs·문서 헤더·컷코너·스탬프 스니펫이 Task 3~6의 시각 기준 (각 태스크에 좌표 조정본 재수록됨).

**보존 문구 (전부 존재해야 함):** `SHEET 01 / 05`, `TAEHYEONG LIM, PH.D.`, `HUMAN × AI`, `CO-INTELLIGENCE SYSTEMS`, `Building multi-agent systems that think, verify, and work with humans.`, `AI CO-SCIENTIST`, `MULTI-AGENT SYSTEMS`, `HUMAN-IN-THE-LOOP`, `HUMAN INTENT`, `AI AGENCY`, `CO-INTELLIGENCE LATTICE / 01`, `FIG.01`
**신규 문구:** 다크 스테이터스 라인 `SYSTEM NOMINAL · 45 AGENTS ACTIVE`, 일본어 서브라벨 `協働知能システム` (양 모드), `DOC NO. NERV-TL-2026-01`, `REV 2026.07`, `MAGI CHECKED`

- [ ] **Step 1: 디스플레이 타이포 패스 생성**

```bash
cd /Users/taehyeong/Documents/GitHub/taehyeonglim
SCRATCH=/private/tmp/claude-501/-Users-taehyeong-Documents-GitHub-cv/a8eda218-dad1-4cbe-ad9f-5bbbb5c5efa9/scratchpad
python3 scripts/textpath.py "$SCRATCH/ChakraPetch-SemiBold.ttf" "HUMAN × AI" 64 0.02 > "$SCRATCH/t-human.txt"
python3 scripts/textpath.py "$SCRATCH/ChakraPetch-SemiBold.ttf" "CO-INTELLIGENCE SYSTEMS" 34 0.04 > "$SCRATCH/t-cosys.txt"
head -1 "$SCRATCH/t-human.txt" "$SCRATCH/t-cosys.txt"
```

Expected: 각 파일 1행에 `<!-- width=NNN.N -->` (좌측 타이포 블록 폭 산정에 사용), 2행에 d 문자열. `×`(U+00D7) 글리프가 없으면 `HUMAN`, `AI`를 따로 변환하고 `×`는 두 획 `<path d="M0 0L18 18M18 0L0 18" stroke="#ff3b30" stroke-width="4"/>`로 직접 그린다.

- [ ] **Step 2: `hero-dark.svg` 조판**

전체 교체. 아래 스캐폴드는 그대로 쓰고, `<!-- 조판 -->` 영역만 배치 감각에 따라 구성한다.

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="320" viewBox="0 0 1200 320" role="img" aria-labelledby="title desc">
<title id="title">Taehyeong Lim — Human × AI Co-Intelligence Systems</title>
<desc id="desc">MAGI terminal-style hero panel. FIG.01 of a five-sheet NERV document set.</desc>
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#050609"/><stop offset="1" stop-color="#0a0c12"/>
  </linearGradient>
  <radialGradient id="redGlow" cx=".5" cy="-.2" r="1">
    <stop offset="0" stop-color="#d92720" stop-opacity=".11"/>
    <stop offset="1" stop-color="#d92720" stop-opacity="0"/>
  </radialGradient>
  <pattern id="gridFine" width="8" height="8" patternUnits="userSpaceOnUse">
    <path d="M8 0H0V8" fill="none" stroke="#f4efe6" stroke-opacity=".03"/>
  </pattern>
  <pattern id="gridBold" width="40" height="40" patternUnits="userSpaceOnUse">
    <path d="M40 0H0V40" fill="none" stroke="#f4efe6" stroke-opacity=".05"/>
  </pattern>
  <style>
    text{font-family:ui-monospace,'SF Mono',SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace;}
    .scan{animation:scan 16s linear infinite;}
    @keyframes scan{to{transform:translateX(1180px);}}
    .blink{animation:blink 2.4s steps(2,start) infinite;}
    @keyframes blink{50%{opacity:.25;}}
    @media (prefers-reduced-motion:reduce){.scan,.blink{animation:none;}}
  </style>
</defs>
<rect width="1200" height="320" fill="url(#bg)"/>
<rect width="1200" height="320" fill="url(#redGlow)"/>
<rect width="1200" height="320" fill="url(#gridFine)"/>
<rect width="1200" height="320" fill="url(#gridBold)"/>
<line x1="0" y1="100" x2="1200" y2="100" stroke="#ff3b30" stroke-opacity=".16"/>
<rect x="2" y="2" width="1196" height="316" fill="none" stroke="#d8d5ce" stroke-opacity=".6" stroke-width="2.5"/>
<rect x="10" y="10" width="1180" height="300" fill="none" stroke="#d8d5ce" stroke-opacity=".28"/>
<rect class="scan" x="10" y="10" width="1" height="300" fill="#f4efe6" fill-opacity=".16"/>
<!-- 조판: 아래 요소들을 배치 -->
<!-- ① 상단 좌측 스테이터스 라인 -->
<circle class="blink" cx="60" cy="40" r="3" fill="#34d399"/>
<text x="72" y="44" font-size="10" letter-spacing="2" fill="#8d9098">SYSTEM NOMINAL · 45 AGENTS ACTIVE</text>
<!-- ② 상단 우측: SHEET 01 / 05 (font-size 9.5, letter-spacing 2, fill #5c6069, text-anchor end) -->
<!-- ③ 좌측 타이포 블록: eyebrow TAEHYEONG LIM, PH.D. (10px, ls 3, #8d9098) →
     HUMAN × AI (Step 1 패스, fill #f4efe6, × 부분만 #ff3b30) →
     CO-INTELLIGENCE SYSTEMS (Step 1 패스, fill #f4efe6) →
     일본어 서브라벨 協働知能システム (11px, ls 4, #5c6069, font-family에 'Hiragino Kaku Gothic ProN',sans-serif 추가) →
     서브 문구 Building multi-agent systems... (12px, #d8d5ce) -->
<!-- ④ 캡슐 3개: AI CO-SCIENTIST / MULTI-AGENT SYSTEMS / HUMAN-IN-THE-LOOP —
     컷코너 라벨(컷 6px): <path d="M{x0+6} {y0}H{x1}V{y1-6}L{x1-6} {y1}H{x0}V{y0+6}Z" fill="none" stroke="#780f10" stroke-width="1.5"/> + 내부 텍스트 10px ls 2 #d8d5ce -->
<!-- ⑤ 우측 HUD 레티클: 기존 크로스헤어 원 2개 구도 유지 — 원(#d8d5ce, op .5) + 십자선 + 눈금 틱,
     라벨 HUMAN INTENT / AI AGENCY (9px, #8d9098), 중앙 × (#ff3b30), HUMAN / AI / × 노드 라벨,
     하단 캡션 CO-INTELLIGENCE LATTICE / 01 (9px, ls 2, #5c6069), 연결선 1개에 stroke-dasharray="4 6" -->
<!-- ⑥ 문서 헤더 (하단 우측) -->
<g font-size="8">
  <rect x="808" y="284" width="382" height="24" fill="none" stroke="#d8d5ce" stroke-opacity=".5"/>
  <path d="M872 284v24M1020 284v24M1084 284v24" stroke="#d8d5ce" stroke-opacity=".35"/>
  <text x="840" y="299" text-anchor="middle" font-weight="800" letter-spacing="1" fill="#ff3b30">FIG.01</text>
  <text x="946" y="299" text-anchor="middle" fill="#8d9098">DOC NO. NERV-TL-2026-01</text>
  <text x="1052" y="299" text-anchor="middle" fill="#8d9098">REV 2026.07</text>
  <text x="1137" y="299" text-anchor="middle" fill="#8d9098">MAGI CHECKED</text>
</g>
</svg>
```

- [ ] **Step 3: `hero-light.svg` 조판 — 동일 지오메트리, 공문서 치환**

다크본을 복사한 뒤 치환표 적용:

| 다크 | 라이트 |
|---|---|
| bg 그라데이션 `#050609/#0a0c12` | `#f4efe6/#ece5d8` |
| `redGlow` rect | 삭제 |
| 그리드 `#f4efe6` op `.03/.05` | `#1a1b1e` op `.08/.12` |
| 레드 축선 `#ff3b30` op `.16` | `#d92720` op `.14` |
| 프레임·본문 `#d8d5ce` | `#2a2b30` |
| 제목 잉크 `#f4efe6` | `#1a1b1e` |
| muted `#8d9098` / dim `#5c6069` | `#6b6558` |
| 레드 `#ff3b30` / 딥 `#780f10` | `#d92720` |
| `.scan` rect, `<style>`의 animation 3종, `class="blink"` | 전부 삭제 (`<style>`은 font-family 1줄만 남김) |
| ① 스테이터스 라인 (그린 dot + SYSTEM NOMINAL) | 삭제하고 레터헤드로 교체: `<text x="60" y="44" font-size="10" letter-spacing="3" fill="#6b6558">NERV · FUTURE LEARNING SYSTEMS DIVISION</text>` + 아래 레드 등록선 `<line x1="60" y1="52" x2="320" y2="52" stroke="#d92720" stroke-width="2"/>` |
| (없음) | 우상단 스탬프 추가: `<g transform="rotate(-4 1080 60)"><rect x="1010" y="38" width="140" height="44" fill="none" stroke="#d92720" stroke-width="2.5" stroke-opacity=".85" rx="3"/><text x="1080" y="56" text-anchor="middle" font-size="11" font-weight="800" letter-spacing="2" fill="#d92720" fill-opacity=".9">MAGI</text><text x="1080" y="72" text-anchor="middle" font-size="11" font-weight="800" letter-spacing="2" fill="#d92720" fill-opacity=".9">CHECKED</text></g>` (SHEET 01 / 05 라벨과 겹치면 SHEET 라벨을 좌측으로 이동) |
| desc "MAGI terminal-style" | "NERV printed-document style" |

- [ ] **Step 4: 구조 검증**

```bash
xmllint --noout assets/hero-dark.svg && xmllint --noout assets/hero-light.svg
grep -c '協働知能システム' assets/hero-dark.svg assets/hero-light.svg   # 각 1
grep -c 'SYSTEM NOMINAL' assets/hero-dark.svg                            # 1
grep -c 'animation' assets/hero-light.svg                                # 0 (grep 종료코드 1)
grep -o 'href="http[^"]*"' assets/hero-*.svg                             # 출력 없음
grep -c 'prefers-reduced-motion' assets/hero-dark.svg                    # 1
for s in "SHEET 01 / 05" "TAEHYEONG LIM" "HUMAN INTENT" "AI AGENCY" "CO-INTELLIGENCE LATTICE / 01" "DOC NO. NERV-TL-2026-01" "MAGI CHECKED"; do grep -L "$s" assets/hero-dark.svg assets/hero-light.svg; done  # 출력 없음(전부 존재)
```

- [ ] **Step 5: 시각 검증**

```bash
SCRATCH=/private/tmp/claude-501/-Users-taehyeong-Documents-GitHub-cv/a8eda218-dad1-4cbe-ad9f-5bbbb5c5efa9/scratchpad
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless --disable-gpu --screenshot="$SCRATCH/hero-dark.png" --window-size=1200,320 "file:///Users/taehyeong/Documents/GitHub/taehyeonglim/assets/hero-dark.svg"
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless --disable-gpu --screenshot="$SCRATCH/hero-light.png" --window-size=1200,320 "file:///Users/taehyeong/Documents/GitHub/taehyeonglim/assets/hero-light.svg"
```

두 PNG를 Read로 열어 확인: 텍스트 겹침 없음, 패스 타이포 렌더 정상, 다크/라이트 각각 터미널/공문서로 읽히는지, 대비 충분한지.

- [ ] **Step 6: 커밋**

```bash
git add assets/hero-dark.svg assets/hero-light.svg
git commit -m "feat(assets): NERV reskin — hero (FIG.01)

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

- [ ] **Step 7: 🛑 시안 게이트 — 사용자 승인**

두 PNG를 사용자에게 제시하고 승인받는다. **승인 전 Task 3 이후 진행 금지.** 수정 요청 시 이 태스크 안에서 반복 후 재커밋(`--amend` 가능, push 전이므로 안전).

---

### Task 3: 버튼 3종 (6파일)

**Files:**
- Modify: `assets/btn-whitepaper-dark.svg` / `-light.svg` (viewBox `0 0 172 34`)
- Modify: `assets/btn-agents-dark.svg` / `-light.svg` (viewBox `0 0 148 34`)
- Modify: `assets/btn-magi-dark.svg` / `-light.svg` (viewBox `0 0 172 34`)

**Interfaces:**
- Consumes: Task 2 승인으로 확정된 팔레트·컷코너 문법.

**보존 문구:** `NERV WHITEPAPER` / `45 AI AGENTS` / `MAGI VALIDATION` (각 버튼 1개)

- [ ] **Step 1: 다크 3본 조판** — 공통 템플릿 (W=172 예시, btn-agents는 W=148로 치환):

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="172" height="34" viewBox="0 0 172 34" role="img" aria-labelledby="title">
<title id="title">NERV WHITEPAPER</title>
<defs><style>text{font-family:ui-monospace,'SF Mono',SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace;}</style></defs>
<rect width="172" height="34" fill="#0a0c12"/>
<path d="M7 1H165L171 7V27L165 33H7L1 27V7Z" fill="none" stroke="#d92720" stroke-width="1.5"/>
<path d="M7 1H165L171 7V27L165 33H7L1 27V7Z" fill="none" stroke="#ff3b30" stroke-opacity=".35" stroke-width="4"/>
<circle cx="14" cy="17" r="2" fill="#ff3b30"/>
<text x="93" y="21" text-anchor="middle" font-size="10.5" font-weight="700" letter-spacing="2" fill="#f4efe6">NERV WHITEPAPER</text>
</svg>
```

글로우는 두 번째 path(굵은 저투명 스트로크)로 표현 — filter 미사용(래스터화 안정성). 좌측 dot은 정적(모션 금지). 각 버튼의 `<title>`·텍스트만 교체: `45 AI AGENTS`(x중앙 81), `MAGI VALIDATION`.

- [ ] **Step 2: 라이트 3본 조판** — 치환: 바탕 `#f4efe6`, 아웃라인 `#1a1b1e`(글로우 path 삭제), dot `#d92720`, 텍스트 `#1a1b1e`.

- [ ] **Step 3: 검증**

```bash
for f in assets/btn-*.svg; do xmllint --noout "$f" || echo "FAIL $f"; done
grep -c 'animation' assets/btn-*.svg | grep -v ':0' || true   # 출력 없음(전부 0)
SCRATCH=/private/tmp/claude-501/-Users-taehyeong-Documents-GitHub-cv/a8eda218-dad1-4cbe-ad9f-5bbbb5c5efa9/scratchpad
for f in btn-whitepaper-dark btn-whitepaper-light btn-agents-dark btn-agents-light btn-magi-dark btn-magi-light; do
  W=172; case $f in btn-agents-*) W=148;; esac
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless --disable-gpu --screenshot="$SCRATCH/$f.png" --window-size=$W,34 "file:///Users/taehyeong/Documents/GitHub/taehyeonglim/assets/$f.svg"
done
```

6개 PNG Read로 육안 확인 (텍스트 잘림·컷코너 형태).

- [ ] **Step 4: 커밋**

```bash
git add assets/btn-*.svg
git commit -m "feat(assets): NERV reskin — badge buttons

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 4: FIG.02 연구 지도 쌍

**Files:**
- Modify: `assets/research-map-dark.svg` / `-light.svg` (viewBox `0 0 1200 440`)

**Interfaces:**
- Consumes: Task 2의 defs·문서 헤더 스니펫 (아래에 좌표 조정본 수록).

**보존 문구:** `AI SYSTEMS ARCHITECTURE`, `SHEET 02 / 05`, `NERV / MAGI`, `AI Co-Scientist`, `orchestrate · verify · remember · act`, `ø45 AGENTS`, `PT-01`~`PT-06`, `Multi-Agent Orchestration`, `Tool-Using Agents`, `Autonomous Validation`, `Long-Term Memory`, `Human in the Loop`, `Research Automation`, `roles · routing · handoffs`, `actions · APIs · workflows`, `critique · consensus · checks`, `context · retrieval · continuity`, `judgment · control · oversight`, `literature · data · writing`, `COMMAND FLOW`, `VALIDATION FEEDBACK`, `FIG.02`

- [ ] **Step 1: 다크본 조판** — 기존 다크본의 지오메트리(허브-스포크 배치·직교 배선 경로 좌표)를 최대한 재사용하고 스킨만 교체한다:
  - defs·배경·그리드·프레임·스캔라인: Task 2 Step 2 스캐폴드와 동일 (height 440으로: 배경 rect `1200×440`, 내부 프레임 `10 10 1180 420`, 스캔 rect height 420, 레드 축선 y=140).
  - 모듈 박스 6개 → 컷코너 패널(컷 8px, stroke `#d8d5ce` op .6), 파트넘버를 브래킷 라벨로: `PT-01` → `[ PT-01 ]` (10px, ls 1, fill `#ffb000` 아님 — **앰버 금지, `#8d9098`**).
  - 중앙 허브 → 이중 컷코너 패널(컷 14px), 제목 `NERV / MAGI` (14px bold ls 2 `#f4efe6`), 서브 2줄 유지, `ø45 AGENTS` 치수 표기 유지(9px `#5c6069`).
  - **`Human in the Loop` 박스만 레드**: stroke `#ff3b30` op .8, 파트넘버·제목 fill `#ff3b30`, 마커 dot에 `class="blink"`.
  - 배선: COMMAND FLOW = 실선 `#d8d5ce` op .5 / VALIDATION FEEDBACK = 점선 `stroke-dasharray="4 6"` `#ff3b30` op .5. 범례 우상단 유지.
  - 문서 헤더: Task 2 Step 2 ⑥과 동일 구조, y=404 (`284→404`), `FIG.02`, `DOC NO. NERV-TL-2026-02`.
  - `<title>`: `AI systems architecture — NERV / MAGI co-scientist`, `<desc>`: `MAGI terminal-style orthogonal wiring diagram. FIG.02 of 5.`

- [ ] **Step 2: 라이트본 조판** — Task 2 Step 3 치환표 그대로 적용 + HITL 레드는 `#d92720`. blink 삭제. 스탬프는 이 자산엔 넣지 않는다(다이어그램 밀도 높음).

- [ ] **Step 3: 검증** — Task 2 Step 4·5와 동일 패턴. 스크린샷 `--window-size=1200,440`, 파일명 `research-map-{dark,light}.png`. 보존 문구 루프에 위 목록 전체 사용. `grep -c 'animation' assets/research-map-light.svg` → 0.

- [ ] **Step 4: 커밋**

```bash
git add assets/research-map-dark.svg assets/research-map-light.svg
git commit -m "feat(assets): NERV reskin — research map (FIG.02)

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 5: FIG.03 NERV 카드 쌍

**Files:**
- Modify: `assets/project-nerv-dark.svg` / `-light.svg` (viewBox `0 0 1200 270`)

**Interfaces:**
- Consumes: Task 1 CLI (타이틀 패스), Task 2 스니펫 (좌표 조정본 수록).

**보존 문구:** `SHEET 03 / 05`, `NERV TECHNICAL WHITEPAPER`(eyebrow — 기존 `AI CO-SCIENTIST SYSTEM`과 역할 교대), `AI CO-SCIENTIST SYSTEM`(메인 타이틀로 승격), `NERV SYSTEM WHITEPAPER`(패널 내 라벨로 유지), `A 45-agent AI co-scientist for complex research workflows.`, `Role-based agents · autonomous cross-validation · research workflow orchestration`, `45 AI AGENTS`, `7 SYSTEM ROLES`, `MAGI VALIDATION`, `RESEARCH`, `CORE`, `ø 7 ROLES`, `MAGI`, `VALIDATED`, `READ THE WHITEPAPER →`, `FIG.03`

- [ ] **Step 1: 타이틀 패스 생성**

```bash
SCRATCH=/private/tmp/claude-501/-Users-taehyeong-Documents-GitHub-cv/a8eda218-dad1-4cbe-ad9f-5bbbb5c5efa9/scratchpad
python3 scripts/textpath.py "$SCRATCH/ChakraPetch-SemiBold.ttf" "AI CO-SCIENTIST SYSTEM" 40 0.03 > "$SCRATCH/t-coscientist.txt"
```

- [ ] **Step 2: 다크본 조판** — whitepaper 랜딩 미러링이 목적:
  - 전체를 32px 컷코너 대형 패널 1장으로: `<path d="M42 10H1158L1190 42V228L1158 260H42L10 228V42Z" fill="#121419" fill-opacity=".6" stroke="#d8d5ce" stroke-opacity=".6" stroke-width="2"/>` (배경·그리드·스캔라인은 Task 2 스캐폴드, height 270).
  - 좌측: eyebrow `NERV TECHNICAL WHITEPAPER` (10px, ls 3, `#ff3b30`) → 메인 타이틀 패스(Step 1, fill `#f4efe6`) → 설명 2줄(12px `#d8d5ce`) → 캡슐 3개(Task 2 ④ 문법) → CTA `READ THE WHITEPAPER →` (11px bold ls 2, `#ff3b30`).
  - 우측: 방사형 7노드 구도 유지 — 중앙 `RESEARCH`/`CORE` 2줄 + 방사 인출선 7개 + `ø 7 ROLES` 치수 + `NERV SYSTEM WHITEPAPER` 캡션(9px ls 2 `#5c6069`).
  - `MAGI VALIDATED` 글로우 배지(우상단): Task 2 Step 3 스탬프 구조에서 stroke `#ff3b30`, 이중 스트로크(안쪽 1.5px op .85 + 바깥 4px op .25)로 글로우, 회전 없이 수평.
  - 문서 헤더 y=234, `FIG.03`, `DOC NO. NERV-TL-2026-03`.
  - `<desc>`: `MAGI terminal-style whitepaper card. FIG.03 of 5.`

- [ ] **Step 3: 라이트본 조판** — Task 2 Step 3 치환표 + 패널 fill `#ece5d8` op .5 + `MAGI VALIDATED`는 회전 -4° 레드 스탬프(Task 2 Step 3 스니펫, 문구만 MAGI / VALIDATED).

- [ ] **Step 4: 검증** — 스크린샷 `--window-size=1200,270`. 보존 문구 루프. `grep -c 'animation' assets/project-nerv-light.svg` → 0.

- [ ] **Step 5: 커밋**

```bash
git add assets/project-nerv-dark.svg assets/project-nerv-light.svg
git commit -m "feat(assets): NERV reskin — whitepaper card (FIG.03)

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 6: FIG.04 필드 리절트 쌍

**Files:**
- Modify: `assets/field-results-dark.svg` / `-light.svg` (viewBox `0 0 1200 200`)

**Interfaces:**
- Consumes: Task 2 스니펫 (좌표 조정본 수록).
- Produces: **R-02 행 추가가 쉬운 구조** — R-01 행 전체를 `<g id="row-r01" transform="translate(0,0)">`로 묶어, 8월에 `row-r02` 복제 + translate + height 확장만으로 추가 가능해야 한다.

**보존 문구:** `SHEET 04 / 05`, `FIELD RESULTS`, `R-01`, `Building an agentic AI-based co-researcher system:`, `An autoethnographic reflection of an educational technology researcher`, `Lim, T. · The Journal of Educational Information and Media · 32(2), 701–728 · KCI · in Korean`, `DOI 10.15833/KAFEIAM.32.2.701`, `PUBLISHED 2026.04`, `READ THE PAPER →`, `FIG.04`

- [ ] **Step 1: 다크본 조판** — 게재 실적 터미널 readout:
  - 배경·그리드·프레임·스캔: Task 2 스캐폴드 (height 200, 스캔 rect height 180, 레드 축선 생략 — 낮은 높이).
  - 헤더 라인: `FIELD RESULTS` (12px bold ls 3 `#f4efe6`) + 우측 `SHEET 04 / 05`.
  - R-01 행: `<g id="row-r01">` — 브래킷 라벨 `[ R-01 ]` (bold `#ff3b30`) + 제목 2줄(12px `#f4efe6`) + 서지 1줄(10px `#8d9098`) + `DOI 10.15833/KAFEIAM.32.2.701` (10px `#d8d5ce`) + 우측 `PUBLISHED 2026.04` 컷코너 라벨(Task 2 ④ 문법, stroke `#34d399` 아님 — **그린 금지, `#780f10`**) + `READ THE PAPER →` (`#ff3b30`).
  - 문서 헤더 y=164, `FIG.04`, `DOC NO. NERV-TL-2026-04`.
  - `<desc>`: `MAGI terminal-style publication record. FIG.04 of 5.`

- [ ] **Step 2: 라이트본 조판** — 게재 증명 공문서: Task 2 Step 3 치환표 + `PUBLISHED 2026.04`를 회전 -3° 레드 스탬프로(테두리+텍스트 `#d92720`).

- [ ] **Step 3: 검증** — 스크린샷 `--window-size=1200,200`. 보존 문구 루프 + `grep -c 'id="row-r01"' assets/field-results-*.svg` → 각 1. `grep -c 'animation' assets/field-results-light.svg` → 0.

- [ ] **Step 4: 커밋**

```bash
git add assets/field-results-dark.svg assets/field-results-light.svg
git commit -m "feat(assets): NERV reskin — field results (FIG.04)

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 7: FIG.05 액티비티 차트 — `generate_activity.py` 리스킨 (TDD)

**Files:**
- Modify: `scripts/generate_activity.py`
- Modify: `tests/test_generate_activity.py`

**Interfaces:**
- Consumes: 없음 (독립).
- Produces: `PALETTES["dark"|"light"]`에 신규 키 `bar`(막대색), `scan`(bool, 스캔라인 유무). `render_svg` 출력에 `DOC NO. NERV-TL-2026-05` 헤더.

- [ ] **Step 1: 테스트 갱신 (실패 유도)** — `tests/test_generate_activity.py`에서:

기존 `test_palettes_differ`의 색 단언을 교체하고 신규 테스트 2개 추가 (파일 상단의 기존 import·헬퍼는 그대로 사용, `render(p)`는 이 파일의 기존 렌더 호출 관례를 따라 작성):

```python
    def test_palettes_differ(self):
        dark = ga.render_svg(self.weeks, self.total, ga.PALETTES["dark"])
        light = ga.render_svg(self.weeks, self.total, ga.PALETTES["light"])
        self.assertIn("#050609", dark)      # MAGI 보이드
        self.assertIn("#ece5d8", light)     # 공문서 음영
        self.assertIn("#ffb000", dark)      # 앰버 막대 (다크 전용)
        self.assertNotIn("#ffb000", light)  # 라이트 2색 원칙
        self.assertNotEqual(dark, light)

    def test_dark_only_motion(self):
        dark = ga.render_svg(self.weeks, self.total, ga.PALETTES["dark"])
        light = ga.render_svg(self.weeks, self.total, ga.PALETTES["light"])
        self.assertIn('class="scan"', dark)
        self.assertNotIn("animation", light)

    def test_nerv_doc_header(self):
        svg = ga.render_svg(self.weeks, self.total, ga.PALETTES["dark"])
        self.assertIn("DOC NO. NERV-TL-2026-05", svg)
        self.assertIn("MAGI CHECKED", svg)
        self.assertNotIn("DWG NO.", svg)
        self.assertNotIn("SCALE 1:1", svg)
```

(기존 파일이 `ga.` 별칭이 아니면 해당 파일의 import 방식에 맞춰 동일 의미로 작성. `self.weeks`/`self.total` 픽스처는 기존 setUp 재사용.)

- [ ] **Step 2: 실패 확인**

Run: `python3 -m unittest tests.test_generate_activity -v`
Expected: FAIL — `test_palettes_differ`(#050609 없음), `test_dark_only_motion`(light에 animation 존재), `test_nerv_doc_header`(DWG NO. 존재)

- [ ] **Step 3: 구현** — `scripts/generate_activity.py`:

① docstring(1~3행)의 `FIG.04` → `FIG.05`, `blueprint-style` → `NERV MAGI-terminal style` 문구 정리.

② `PALETTES` 전체 교체:

```python
PALETTES = {
    "dark": {   # MAGI 터미널
        "bg0": "#050609", "bg1": "#0a0c12", "grid": "#f4efe6",
        "grid_fine": ".03", "grid_bold": ".05", "ink": "#d8d5ce",
        "strong": "#f4efe6", "mid": "#8d9098", "dim": "#5c6069",
        "bar": "#ffb000", "red": "#ff3b30",
        "frame_op": ".6", "scan_op": ".16", "scan": True,
    },
    "light": {  # NERV 공문서 — 먹+레드 2색
        "bg0": "#f4efe6", "bg1": "#ece5d8", "grid": "#1a1b1e",
        "grid_fine": ".08", "grid_bold": ".12", "ink": "#2a2b30",
        "strong": "#1a1b1e", "mid": "#6b6558", "dim": "#6b6558",
        "bar": "#2a2b30", "red": "#d92720",
        "frame_op": ".55", "scan_op": "0", "scan": False,
    },
}
```

③ `render_svg` 수정 4곳:
- `<desc>`(77~78행): `'MAGI terminal-style bar chart of weekly GitHub contributions over the last year. FIG.05 of 5.'`
- `<style>` 블록(87~92행): `p["scan"]`이 False면 `.scan` 규칙·keyframes를 출력하지 않도록 조건 분기 (font-family 줄은 항상 출력).
- 스캔라인 rect(106~107행): `if p["scan"]:` 안으로 이동.
- 막대 색(144행): `color = p["red"] if i == peak_i else p["bar"]`
- 타이틀 블록(168~179행): 4번째 셀 `SCALE 1:1` → `MAGI CHECKED`, `DWG NO. TL-2026-05` → `DOC NO. NERV-TL-2026-05` (칸 폭이 부족하면 rect x를 848, 구획선 x를 좌로 8px씩 이동).

- [ ] **Step 4: 전체 테스트 통과 확인**

Run: `python3 -m unittest discover -s tests -v`
Expected: `OK` — test_generate_activity 9개(기존 7 + 신규 2) + test_textpath 3개 전부 PASS

- [ ] **Step 5: 실데이터 렌더 + 시각 검증**

```bash
SCRATCH=/private/tmp/claude-501/-Users-taehyeong-Documents-GitHub-cv/a8eda218-dad1-4cbe-ad9f-5bbbb5c5efa9/scratchpad
GITHUB_TOKEN=$(gh auth token) python3 scripts/generate_activity.py --user taehyeonglim --out "$SCRATCH/activity"
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless --disable-gpu --screenshot="$SCRATCH/activity-dark.png" --window-size=1200,340 "file://$SCRATCH/activity/build-activity-dark.svg"
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless --disable-gpu --screenshot="$SCRATCH/activity-light.png" --window-size=1200,340 "file://$SCRATCH/activity/build-activity.svg"
```

(출력 파일 배치는 `--out` 기존 동작을 따른다 — `--fixture` 테스트가 두 파일명을 검증하므로 그대로.) 두 PNG Read로 확인. **주의: 로컬 토큰은 비공개 기여 포함 → 라이브(공개만)와 수치 다른 게 정상** (메모리 기록).

- [ ] **Step 6: 커밋**

```bash
git add scripts/generate_activity.py tests/test_generate_activity.py
git commit -m "feat(activity): NERV MAGI-terminal palettes for FIG.05 chart

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 8: 전체 검증 → 최종 게이트 → 배포

**Files:**
- 수정 없음 (검증·push·라이브 확인·메모리 갱신)

**Interfaces:**
- Consumes: Task 1~7의 전체 산출물.

- [ ] **Step 1: 불변 조건 검증**

```bash
cd /Users/taehyeong/Documents/GitHub/taehyeonglim
git status --short                          # 클린
git diff origin/main..HEAD --stat           # README.md·.github 없음 확인
git log origin/main..HEAD --oneline         # 스펙 + 커밋 7개
grep -c 'animation' assets/*-light.svg | grep -v ':0' || echo "OK: light 전부 정적"
grep -o 'href="http[^"]*"' assets/*.svg || echo "OK: 외부 참조 없음"
grep -rn '協働' assets/ | grep -cv 'hero'   # 0 — 일본어는 히어로만
```

- [ ] **Step 2: 전 자산 스크린샷 일람 재생성** — Task 2~6의 스크린샷 명령을 전부 재실행(총 14장)하고, 각 PNG를 Read로 최종 확인 (다크·라이트 톤 일관성, FIG 연번, 문서 헤더 통일).

- [ ] **Step 3: 🛑 최종 게이트 — 사용자 승인**

전 자산 스크린샷을 사용자에게 제시. **승인 전 push 금지.**

- [ ] **Step 4: push + Actions 트리거**

```bash
git push origin main
gh workflow run blueprint-activity.yml
gh run watch $(gh run list --workflow=blueprint-activity.yml --limit 1 --json databaseId -q '.[0].databaseId') --exit-status
```

Expected: push 성공, 워크플로 run 성공(output 브랜치에 NERV 팔레트 SVG 2본).

- [ ] **Step 5: 라이브 확인**

```bash
curl -sI "https://raw.githubusercontent.com/taehyeonglim/taehyeonglim/main/assets/hero-dark.svg" | head -1        # 200
curl -sI "https://raw.githubusercontent.com/taehyeonglim/taehyeonglim/output/build-activity.svg" | head -1        # 200
curl -s "https://raw.githubusercontent.com/taehyeonglim/taehyeonglim/output/build-activity.svg" | grep -c ffb000  # ≥1 (앰버 반영)
```

github.com/taehyeonglim 라이브 프로필 육안 확인 (camo 캐시로 몇 분 지연 가능 — 미갱신 시 기다렸다 재확인).

- [ ] **Step 6: 메모리 갱신** — `/Users/taehyeong/.claude/projects/-Users-taehyeong-Documents-GitHub-cv/memory/project_github_profile_blueprint.md`를 NERV 리스킨 완료 상태로 갱신: 테마=NERV(다크 MAGI 터미널·모션 / 라이트 공문서·정적), `textpath.py` 도구 존재, 문서 헤더 4칸 체계, FIG.04 R-02 PENDING 유지, `MEMORY.md` 인덱스 한 줄도 테마 표기 갱신.

---

## Self-Review 기록

- **스펙 커버리지**: §2 공통 시스템 → Task 2(스캐폴드)+Global Constraints / §3 FIG.01~05·버튼 → Task 2~7 / §4 파이프라인 불변 → Task 8 Step 1 / §6 검증·시안 게이트 2단계 → Task 2 Step 7 + Task 8 Step 3 / §5 폴백 → Global Constraints 타이포 항목. 커버 완료.
- **타입 일관성**: `text_to_path` 시그니처 Task 1↔2↔5 일치. `PALETTES` 신규 키(`bar`, `scan`) Task 7 테스트↔구현 일치. 문서 헤더 4칸 문구 Task 2·4·5·6·7 동일.
- **플레이스홀더**: 조판 자유 영역은 좌표·색·문구·검증 기준을 명시한 구성 지시로 한정 — 시각 게이트(스크린샷 Read + 사용자 승인 2회)가 품질 검증을 담당.
