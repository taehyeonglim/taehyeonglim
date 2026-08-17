# 프로필 README — OPEN SOURCE 섹션 디자인 스펙

- 날짜: 2026-08-17
- 선행 스펙: `2026-07-17-nerv-profile-eva-v2-design.md` — **§2 토큰·§3 어휘·§4.1 한글화 규칙을 그대로 계승** (신규 규칙 없음)
- 직접 템플릿: `assets/field-results-dark.svg` (defs·헤더·패널·액센트 바 문법)
- 사용자 지시 원문: "현재 있는 내용은 건들지 말고, 맨 아래에 추가"

## 1. 목적

프로필 README가 NERV 시스템·논문·활동 차트만 노출하고 다른 공개 레포를 전혀 보여주지 않던 문제를 해소한다. 사용자가 직접 선별한 공개 레포 9종을 에바 v2 터미널 룩 그대로 카탈로그 패널 1장 + 클릭 가능한 링크 행으로 README 맨 아래에 추가한다.

## 2. 설계 결정

| # | 결정 | 근거 |
|---|---|---|
| 1 | **엄격한 append** — 기존 README 줄은 단 한 줄도 수정하지 않고 마지막 `</div>` 뒤에 새 섹션을 붙인다 | 사용자 지시를 문자 그대로 따름. 검증은 `git diff README.md`의 삭제 라인 수가 0인지로 한다 (실측: 14 insertions / 0 deletions) |
| 2 | **스타 수(★) 미표기** | 별도 저장소의 값을 하드코딩하면 드리프트가 생긴다 — 프로필 README ↔ 화이트페이퍼에서 링크·에이전트 수가 어긋났던 전례가 있다. 대신 시간이 지나도 변하지 않는 **타입 태그**(`MCP SERVER`, `AGENT SYSTEM`, `CC PLUGIN`, `CLI`, `DATA VIZ`, `WEB SIM`, `ARCHIVE`)를 표기한다. ※ 사용자가 사전 미리보기에서 본 목업에는 ★ 수가 있었으므로 이 차이는 승인 시점에 명시됨 |
| 3 | **다크/라이트 2파일, 내용 완전 동일** | v2 결정(다크 단일 룩 양 모드 공통) 계승. `<picture>` 마크업 유지 목적의 파일 분리일 뿐이며 `cmp`로 동일성을 검증한다 |
| 4 | **textPath·고스트 타이포 미사용** | 대형 디스플레이 타이포가 없는 조밀한 카탈로그 패널이므로 `field-results`와 동일하게 ui-monospace 스택 + 한글 `'Apple SD Gothic Neo','Malgun Gothic','Noto Sans KR',sans-serif` 스택으로 충분 |
| 5 | **설명 문구 50자 하드캡** | SVG `<text>`는 자동 줄바꿈이 없다. 셀 유효폭 316px ÷ 10px 모노스페이스(0.6em ≈ 6px/자) = 52자 한계. 초과 시 패널 밖으로 넘치므로 생성 시 `assert len(desc) <= 50`로 강제 |
| 6 | **신규 스크립트·테스트 없음** | 기존 수제작 SVG 5종과 동일한 관례. 링크는 `scripts/check_links.py`가 `MD_LINK_RE`·`ATTR_RE`로 자동 수집하므로 CI `link-check` 잡이 그대로 커버한다 |

## 3. 캔버스·레이아웃 사양

`assets/open-source-dark.svg` = `assets/open-source-light.svg` (byte-identical)

| 항목 | 값 |
|---|---|
| 캔버스 | 1200 × 460 (`viewBox="0 0 1200 460"`) |
| 배경 레이어 | bg 그라디언트(#050609→#0a0c12) → glow → hexes(오렌지 op .07) → crt 스캔라인 → vig 비네트 |
| 상단 엣지 | 해저드 테이프 `url(#hz)` op .75 (y=2, h=7) + 블랙 룰 |
| 외곽 프레임 | `x=2 y=2 w=1196 h=456`, stroke #ff6a00 op .4, width 2 |
| 좌우 여백 | 54 |
| 셀 | 356 × 106, 간격 12 (가로·세로 공통) |
| 그리드 상단 | y=78 → 행 y = 78 / 196 / 314 (하단 420) |
| 모션 | `.scan` 16s 세로 스캔바 (x=10, h=440) + `prefers-reduced-motion:reduce` 시 정지 |
| 접근성 | `role="img"` + `aria-labelledby="title desc"` + `<title>`/`<desc>` |

### 3.1 존 헤더

- `▣ OPEN SOURCE — 공개 저장소` (x=54, y=48, 13px/800/ls 3) — `▣` #ff6a00, 영문 #ffe2c4, 한글 부제 #9a7048
- 헤더 룰 y=60, 54→1146, #8a3c00 op .7 / 우측 핫 세그먼트 940→1146, #ff2d2d width 2 op .8
- 우상단 `NERV // PUBLIC REPOSITORIES` (9px, ls 2, #9a7048, anchor end)

### 3.2 셀 사양 (셀 원점 x₀, y₀ 기준)

| 요소 | 위치 | 스타일 |
|---|---|---|
| 패널 박스 | x₀, y₀, 356×106 | fill #10131c fill-opacity .85, stroke #ff6a00 op .35, width 1.5 |
| 좌측 액센트 바 | x₀, y₀, 4×106 | fill #ff6a00 opacity .85 |
| 브래킷 태그 `[ OS-0n ]` | x₀+20, y₀+24 | 10px / 800 / ls 1 / #ffb000 |
| 타입 태그 | x₀+336, y₀+24 (anchor end) | 9px / ls 1.5 / #ffb000 fill-opacity .55 (딤 앰버) |
| 레포명 | x₀+20, y₀+50 | 13.5px / 700 / #ffe2c4 / monospace |
| 영문 설명 | x₀+20, y₀+70 | 10px / #d9a877 |
| 카테고리 태그 | x₀+20, y₀+92 | 8.5px / ls 2 / #9a7048 |

각 셀은 `<g id="cell-os-0n">`으로 감싼다 (`field-results`의 `row-r01` 그룹 관례).

### 3.3 하단 캡션

우측 정렬 `NERV // OPEN SOURCE · 공개 가동` (x=1146, y=444, 8.5px, ls 2, #9a7048, 한글 폰트 스택).

## 4. 셀 내용 (확정 문구 — 변경 시 폭 재검증 필요)

| 태그 | 레포 (표시명) | 카테고리 | 타입 | 영문 설명 | 길이 |
|---|---|---|---|---|---|
| OS-01 | `learning-map-mcp` | AGENTS | MCP SERVER | Korean elementary curriculum graph MCP server | 45 |
| OS-02 | `edtech-oracle` | AGENTS | AGENT SYSTEM | 36 EdTech pioneer agents, citation-backed answers | 49 |
| OS-03 | `paper-scout` | RESEARCH | CC PLUGIN | Literature-discovery agents, deterministic APIs | 47 |
| OS-04 | `academic-roots` | RESEARCH | DATA VIZ | Academic genealogy of V. P. Dennen, visualized | 46 |
| OS-05 | `paper-verifier` | RESEARCH | CLI | Deterministic stat-claim & citation audit | 41 |
| OS-06 | `academic-humanizer` | RESEARCH | CLI | Strips AI-tells from drafts, stats intact | 41 |
| OS-07 | `ai-agent-teacher` | EDTECH | WEB SIM | 6D teacher-competency simulation for the AI era | 47 |
| OS-08 | `k-mosaic` | EDTECH | DATA VIZ | Korea multicultural student data explorer | 41 |
| OS-09 | `edtech-pantheon` | EDTECH | ARCHIVE | Visual archive of EdTech pioneers, evidence-backed | 50 |

배치는 카테고리 묶음 순(행 우선): 1행 OS-01~03, 2행 OS-04~06, 3행 OS-07~09.

- OS-05의 `&`는 SVG 안에서 `&amp;`로 이스케이프된다 (XML 웰폼드 조건).
- OS-01의 표시명은 축약형이며 **실제 레포명은 `korean-elementary-learning-map-mcp`** — README 링크는 풀네임을 가리킨다.

## 5. README 변경

파일 끝에 append하는 블록:

- `## Open source` 헤딩
- `<picture>` — dark/light `srcset` + `src`는 light, `width="100%"`, `alt="Open source — nine public repositories across agents, research tools, and edtech"`
- `<div align="center">` 안에 `▸`로 시작하는 9개 레포 링크 행 (`·` 구분)
- 링크는 전부 `https://github.com/taehyeonglim/<풀네임>`, 표시 텍스트만 축약

기존 모토 푸터(`Systems over demos · …`)는 새 섹션 바로 위 원래 자리에 그대로 남는다.

> 대안(미채택): 모토 푸터를 문서 맨 끝에 유지하기 위해 기존 `<div>`를 분리하고 차트와 푸터 사이에 새 섹션을 끼워 넣는 방식. 기존 마크업 수정을 수반하므로 결정 #1에 위배된다. 사용자가 원하면 전환 가능.

## 6. 검증

| # | 검사 | 결과 |
|---|---|---|
| 1 | `python3 -c "import xml.dom.minidom; xml.dom.minidom.parse('assets/open-source-dark.svg')"` (light 동일) | 통과 |
| 2 | `cmp assets/open-source-dark.svg assets/open-source-light.svg` | 동일 |
| 3 | `git diff --numstat README.md` → 삭제 0줄 | 14 insertions / 0 deletions |
| 4 | 세 파일 모두 끝 개행 포함 | 통과 |
| 5 | 가나(U+3040–30FF)·한자(U+4E00–9FFF) 잔재 스캔 (v2.1 규칙) | 0건 (`▣` U+25A3는 기호로 무관) |
| 6 | 설명 문구 ≤ 50자 | 전 9건 통과 |

푸시 이후: `scripts/check_links.py` / CI `link-check` 잡이 9개 레포 URL과 신규 `raw.githubusercontent.com` srcset 3건을 검증한다. 푸시 전 로컬 실행 시 신규 SVG raw URL 3건의 404는 예상된 실패다.

---

## 7. v2 개정 — 9종 → 13종 확장 (2026-08-17)

9pt 플로어 개정(`2026-08-17-typography-9pt-floor-design.md`)으로 확정된 **2열 그리드·셀 540×100·행 피치 112** 문법을 그대로 유지한 채 셀 4종을 추가한다. 폰트 사이즈·색·셀 내부 베이스라인(+23/+48/+71/+92)은 **불변**이며, 확장은 행 추가와 캔버스 높이 재계산만으로 처리한다.

### 7.1 추가 4종

| 태그 | 레포 (표시명) | 카테고리 | 타입 | 영문 설명 | 길이 |
|---|---|---|---|---|---|
| OS-03 | `agent-galaxy` | AI TOOLS | 3D VIZ | Zero-dependency 3D multi-agent visualization | 44 |
| OS-04 | `deck-ai-usage` | AI TOOLS | DECK PLUGIN | AI usage gauges for Elgato Stream Deck | 38 |
| OS-12 | `2026-esports-landscape` | EDTECH | DATA SITE | Korea school-esports landscape, evidence-based | 46 |
| OS-13 | `korean-elementary-textbook` | EDTECH | WORKBOOKS | Free curriculum-aligned elementary workbooks | 44 |

- 신규 카테고리 **AI TOOLS**, 신규 타입 태그 **3D VIZ / DECK PLUGIN / DATA SITE / WORKBOOKS** 추가. 스타 수 미표기(결정 #2) 유지.
- 전 13종 설명 문구가 9pt 스펙의 **46자 캡** 이내 (OS-12가 정확히 46자 — 재작성 시 초과 주의).
- OS-12·OS-13은 표시명이 축약형이며 실제 레포는 `2026-esports-landscape` / `korean-elementary-textbook`. OS-01의 풀네임 규칙(`korean-elementary-learning-map-mcp`)과 동일한 처리다.

### 7.2 셀 재배열 (카테고리 짝 맞춤 — 기존 9종도 번호·위치가 바뀜)

| 행 | y | 좌측 (x=54) | 우측 (x=606) |
|---|---|---|---|
| 1 | 76 | OS-01 `learning-map-mcp` (AGENTS) | OS-02 `edtech-oracle` (AGENTS) |
| 2 | 188 | OS-03 `agent-galaxy` (AI TOOLS) | OS-04 `deck-ai-usage` (AI TOOLS) |
| 3 | 300 | OS-05 `paper-scout` (RESEARCH) | OS-06 `academic-roots` (RESEARCH) |
| 4 | 412 | OS-07 `paper-verifier` (RESEARCH) | OS-08 `academic-humanizer` (RESEARCH) |
| 5 | 524 | OS-09 `ai-agent-teacher` (EDTECH) | OS-10 `k-mosaic` (EDTECH) |
| 6 | 636 | OS-11 `edtech-pantheon` (EDTECH) | OS-12 `2026-esports-landscape` (EDTECH) |
| 7 | 748 | OS-13 `korean-elementary-textbook` (EDTECH) — **중앙 배치 x=330** | — |

배치 원칙: 같은 카테고리끼리 한 행에 짝지어 좌우를 채운다. 13은 홀수이므로 마지막 셀은 v1의 9번째 셀과 동일한 중앙 배치 문법(rect·액센트 x=330, 텍스트 x=350, 타입 태그 anchor-end x=850)을 재사용한다. 그룹 id는 `cell-os-01`~`cell-os-13`.

### 7.3 캔버스 892 근거

v1(9셀)의 668은 `마지막 행 bottom(524+100=624) + 44`로 얻은 값이다. 동일 규칙을 적용한다.

```
마지막 행 top    = 76 + 6×112 = 748
마지막 행 bottom = 748 + 100  = 848
하단 캡션 baseline = 848 + 22 = 870   (= H − 22)
캔버스 높이 H     = 848 + 44  = 892
```

높이에 연동되는 값 전부 갱신: 배경 레이어 5종(bg·glow·hexes·crt·vig) `height=892`, 외곽 프레임 `height=888` (H−4), 스캔바 `height=872` (H−20), 하단 캡션 `y=870`. 상단 해저드 테이프·블랙 룰·존 헤더·헤더 룰·핫 세그먼트는 좌표 불변.

`<title>`/`<desc>`의 "nine" → "thirteen". 일본어·한자 미사용 규칙(v2.1) 유지.

### 7.4 README 변경 (Open source 섹션 한정)

- `<img alt>` "nine public repositories" → "thirteen public repositories"
- `▸` 링크 행을 패널 셀 순서와 동일한 13종으로 **재작성** (append 아님 — `edtech-pantheon`이 9번째에서 11번째로 이동). 표시 텍스트 축약 규칙 유지: `[esports-landscape]` → `2026-esports-landscape`, `[elementary-textbook]` → `korean-elementary-textbook`.
- 실측 diff: 2 insertions / 2 deletions, 전부 Open source 섹션 내부.

### 7.5 v2 검증

| # | 검사 | 결과 |
|---|---|---|
| 1 | `python3 -c "import xml.dom.minidom; xml.dom.minidom.parse('assets/open-source-dark.svg')"` | 통과 |
| 2 | `cmp assets/open-source-dark.svg assets/open-source-light.svg` | 동일 |
| 3 | font-size 값 집합 비교 (HEAD 대비) | `{12, 13, 16, 16.5}` 동일 — 변경 0 |
| 4 | headless Chrome 800px 폭 렌더 육안 확인 | 정렬·중앙 배치 정상, 오버플로 없음 |
| 5 | 신규 4종 레포 존재 (`gh api repos/taehyeonglim/<name>`) | 4/4 확인 |
