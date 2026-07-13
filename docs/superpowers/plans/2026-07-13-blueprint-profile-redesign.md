# Blueprint Profile Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** GitHub 프로필 README의 4개 에셋(히어로/아키텍처/NERV 카드/액티비티 차트)을 엔지니어링 블루프린트 비주얼 아이덴티티로 전면 교체한다.

**Architecture:** 정적 에셋 3쌍(다크=청사진, 라이트=화이트프린트)은 수제 SVG로 교체하고, 액티비티 차트는 Python 표준 라이브러리 스크립트 + GitHub Action이 12시간마다 생성해 output 브랜치에 배포한다. README는 `<picture>` 태그로 모드별 분기한다.

**Tech Stack:** 순수 SVG(CSS `@keyframes` 애니메이션), Python 3 표준 라이브러리(unittest), GitHub Actions.

**Spec:** `docs/superpowers/specs/2026-07-13-blueprint-profile-redesign-design.md`

## Global Constraints

- 작업 브랜치: `redesign/blueprint` (main 병합·push는 Task 6의 사용자 승인 후에만 — push 즉시 공개 프로필에 반영됨)
- 외부 폰트·스크립트 금지. 폰트는 `ui-monospace,'SF Mono',SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace`만 사용
- Python은 표준 라이브러리만 (의존성 0)
- 모든 SVG: `<title>`/`<desc>` 접근성 태그 필수, `@media (prefers-reduced-motion: reduce)`에서 모든 애니메이션 정지
- 다크 팔레트: bg `#0d2a55→#123a75`, 잉크 강 `#eaf2ff`, 중 `#b9d0f0`, 약 `#8fb0dd`, 선 `#dbeafe`, 모눈 `#ffffff` @.04/.07, 레드라인 `#f87171`
- 라이트 팔레트: bg `#ffffff→#f3f7fd`, 잉크 강 `#17337a`, 중 `#2c4d99`, 약 `#6981b8`, 선 `#1e40af`, 모눈 `#1e40af` @.06/.09, 레드라인 `#dc2626`
- 콘텐츠 문구는 기존 README/SVG의 문자열을 그대로 유지 (각 Task에 명시된 문자열 verbatim)
- FIG 연번·타이틀 블록 양식: `FIG.NN / DWG NO. TL-2026-NN / REV 2026.07 / SCALE 1:1`, 우상단 `SHEET NN / 04`
- 애니메이션 어휘(전 에셋 공통 CSS): `.flow`(dash-flow 12s), `.scan`(스캔라인 16s), `.blink`(1.6s steps)

---

### Task 1: FIG.01 — 히어로 배너 SVG 2본

**Files:**
- Create(덮어쓰기): `assets/hero-dark.svg`
- Create(덮어쓰기): `assets/hero-light.svg`

**Interfaces:**
- Consumes: 없음
- Produces: README 기존 `<picture>` 태그가 참조하는 동일 파일명 2개 (README 수정 불필요)

- [ ] **Step 1: `assets/hero-dark.svg` 작성 (전체 내용 교체)**

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="320" viewBox="0 0 1200 320" role="img" aria-labelledby="title desc">
  <title id="title">Taehyeong Lim — Human × AI Co-Intelligence Systems</title>
  <desc id="desc">Blueprint-style dark banner. FIG.01 of a four-sheet drawing set for AI co-scientist builder Taehyeong Lim.</desc>
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#0d2a55"/><stop offset="1" stop-color="#123a75"/>
    </linearGradient>
    <pattern id="gridFine" width="8" height="8" patternUnits="userSpaceOnUse">
      <path d="M8 0H0V8" fill="none" stroke="#ffffff" stroke-opacity=".04"/>
    </pattern>
    <pattern id="gridBold" width="40" height="40" patternUnits="userSpaceOnUse">
      <path d="M40 0H0V40" fill="none" stroke="#ffffff" stroke-opacity=".07"/>
    </pattern>
    <style>
      text { font-family: ui-monospace,'SF Mono',SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace; }
      .flow { stroke-dasharray: 5 7; animation: flow 12s linear infinite; }
      .scan { animation: scan 16s linear infinite; }
      .blink { animation: blink 1.6s steps(1) infinite; }
      @keyframes flow { to { stroke-dashoffset: -96; } }
      @keyframes scan { to { transform: translateX(1180px); } }
      @keyframes blink { 0%, 49% { opacity: 1; } 50%, 100% { opacity: .12; } }
      @media (prefers-reduced-motion: reduce) { .flow, .scan, .blink { animation: none; } }
    </style>
  </defs>
  <rect width="1200" height="320" fill="url(#bg)"/>
  <rect width="1200" height="320" fill="url(#gridFine)"/>
  <rect width="1200" height="320" fill="url(#gridBold)"/>
  <rect x="2" y="2" width="1196" height="316" fill="none" stroke="#dbeafe" stroke-opacity=".6" stroke-width="2.5"/>
  <rect x="10" y="10" width="1180" height="300" fill="none" stroke="#dbeafe" stroke-opacity=".28"/>
  <g stroke="#dbeafe" stroke-opacity=".3" stroke-width="6" stroke-dasharray="1 39">
    <line x1="10" y1="13" x2="1190" y2="13"/>
    <line x1="10" y1="307" x2="1190" y2="307"/>
    <line x1="13" y1="10" x2="13" y2="310"/>
    <line x1="1187" y1="10" x2="1187" y2="310"/>
  </g>
  <g stroke="#dbeafe" stroke-opacity=".45" fill="none">
    <path d="M30 24v12M24 30h12"/><path d="M1170 24v12M1164 30h12"/>
    <path d="M30 284v12M24 290h12"/><path d="M1170 284v12M1164 290h12"/>
  </g>
  <rect class="scan" x="10" y="10" width="1" height="300" fill="#dbeafe" fill-opacity=".16"/>
  <text x="1170" y="42" text-anchor="end" font-size="9.5" letter-spacing="2" fill="#8fb0dd">SHEET 01 / 04</text>
  <text x="68" y="84" font-size="15" font-weight="700" letter-spacing="5" fill="#b9d0f0">TAEHYEONG LIM, PH.D.</text>
  <text x="66" y="152" font-size="50" font-weight="800" letter-spacing="1" fill="#eaf2ff">HUMAN <tspan fill="#f87171">×</tspan> AI</text>
  <text x="68" y="198" font-size="28" font-weight="700" letter-spacing="3" fill="#eaf2ff">CO-INTELLIGENCE SYSTEMS</text>
  <path d="M68 212h438M68 206v12M506 206v12" fill="none" stroke="#dbeafe" stroke-opacity=".5"/>
  <text x="68" y="240" font-size="16" fill="#b9d0f0">Building multi-agent systems that think, verify, and work with humans.</text>
  <g font-size="11" font-weight="700" letter-spacing="1" fill="#b9d0f0">
    <rect x="68" y="264" width="140" height="30" fill="#dbeafe" fill-opacity=".05" stroke="#dbeafe" stroke-opacity=".55"/>
    <text x="138" y="283" text-anchor="middle">AI CO-SCIENTIST</text>
    <rect x="218" y="264" width="178" height="30" fill="#dbeafe" fill-opacity=".05" stroke="#dbeafe" stroke-opacity=".55"/>
    <text x="307" y="283" text-anchor="middle">MULTI-AGENT SYSTEMS</text>
    <rect x="406" y="264" width="164" height="30" fill="#dbeafe" fill-opacity=".05" stroke="#dbeafe" stroke-opacity=".55"/>
    <text x="488" y="283" text-anchor="middle">HUMAN-IN-THE-LOOP</text>
  </g>
  <g fill="none" stroke="#dbeafe">
    <g stroke-opacity=".4" stroke-dasharray="12 4 3 4">
      <path d="M800 140h116M858 82v116"/>
      <path d="M1004 140h116M1062 82v116"/>
    </g>
    <g stroke-opacity=".55" stroke-dasharray="2 5">
      <path d="M858 58v24M1062 58v24"/>
    </g>
    <circle cx="858" cy="53" r="4.5" stroke-opacity=".7"/>
    <circle cx="1062" cy="53" r="4.5" stroke-opacity=".7"/>
    <circle cx="858" cy="140" r="44" stroke-width="2"/>
    <circle cx="1062" cy="140" r="44" stroke-width="2"/>
    <g class="flow" stroke-opacity=".85" stroke-width="1.5">
      <path d="M902 140h45M973 140h45"/>
    </g>
    <circle cx="960" cy="140" r="13" stroke="#f87171" stroke-width="2"/>
    <g stroke-opacity=".6">
      <path d="M827 109l-20 -20h-54"/>
      <path d="M1093 109l20 -20h54"/>
    </g>
    <g stroke-opacity=".45">
      <path d="M858 188v50M1062 188v50"/>
    </g>
    <g stroke-opacity=".8">
      <path d="M858 232h204"/>
      <path d="M866 228l-8 4 8 4M1054 228l8 4-8 4"/>
    </g>
  </g>
  <text x="749" y="93" text-anchor="end" font-size="10" letter-spacing="1.5" fill="#8fb0dd">HUMAN INTENT</text>
  <text x="1117" y="93" font-size="10" letter-spacing="1.5" fill="#8fb0dd">AI AGENCY</text>
  <text x="858" y="145" text-anchor="middle" font-size="11.5" font-weight="800" letter-spacing="1.5" fill="#eaf2ff">HUMAN</text>
  <text x="1062" y="145" text-anchor="middle" font-size="13" font-weight="800" letter-spacing="2" fill="#eaf2ff">AI</text>
  <text x="960" y="145" text-anchor="middle" font-size="15" font-weight="800" fill="#f87171">×</text>
  <circle class="blink" cx="843" cy="223" r="2.5" fill="#f87171"/>
  <text x="960" y="226" text-anchor="middle" font-size="9.5" letter-spacing="2" fill="#8fb0dd">CO-INTELLIGENCE LATTICE / 01</text>
  <g font-size="8.5">
    <rect x="884" y="284" width="306" height="24" fill="none" stroke="#dbeafe" stroke-opacity=".5"/>
    <path d="M946 284v24M1086 284v24M1144 284v24" stroke="#dbeafe" stroke-opacity=".35"/>
    <text x="915" y="299" text-anchor="middle" font-weight="800" letter-spacing="1" fill="#f87171">FIG.01</text>
    <text x="1016" y="299" text-anchor="middle" fill="#b9d0f0">DWG NO. TL-2026-01</text>
    <text x="1115" y="299" text-anchor="middle" fill="#b9d0f0">REV 2026.07</text>
    <text x="1167" y="299" text-anchor="middle" fill="#b9d0f0">SCALE 1:1</text>
  </g>
</svg>
```

- [ ] **Step 2: `assets/hero-light.svg` 작성 (전체 내용 교체)**

다크본과 지오메트리 동일, 팔레트만 화이트프린트. 아래 코드 verbatim:

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="320" viewBox="0 0 1200 320" role="img" aria-labelledby="title desc">
  <title id="title">Taehyeong Lim — Human × AI Co-Intelligence Systems</title>
  <desc id="desc">Whiteprint-style light banner. FIG.01 of a four-sheet drawing set for AI co-scientist builder Taehyeong Lim.</desc>
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="#f3f7fd"/>
    </linearGradient>
    <pattern id="gridFine" width="8" height="8" patternUnits="userSpaceOnUse">
      <path d="M8 0H0V8" fill="none" stroke="#1e40af" stroke-opacity=".06"/>
    </pattern>
    <pattern id="gridBold" width="40" height="40" patternUnits="userSpaceOnUse">
      <path d="M40 0H0V40" fill="none" stroke="#1e40af" stroke-opacity=".09"/>
    </pattern>
    <style>
      text { font-family: ui-monospace,'SF Mono',SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace; }
      .flow { stroke-dasharray: 5 7; animation: flow 12s linear infinite; }
      .scan { animation: scan 16s linear infinite; }
      .blink { animation: blink 1.6s steps(1) infinite; }
      @keyframes flow { to { stroke-dashoffset: -96; } }
      @keyframes scan { to { transform: translateX(1180px); } }
      @keyframes blink { 0%, 49% { opacity: 1; } 50%, 100% { opacity: .12; } }
      @media (prefers-reduced-motion: reduce) { .flow, .scan, .blink { animation: none; } }
    </style>
  </defs>
  <rect width="1200" height="320" fill="url(#bg)"/>
  <rect width="1200" height="320" fill="url(#gridFine)"/>
  <rect width="1200" height="320" fill="url(#gridBold)"/>
  <rect x="2" y="2" width="1196" height="316" fill="none" stroke="#1e40af" stroke-opacity=".55" stroke-width="2.5"/>
  <rect x="10" y="10" width="1180" height="300" fill="none" stroke="#1e40af" stroke-opacity=".25"/>
  <g stroke="#1e40af" stroke-opacity=".3" stroke-width="6" stroke-dasharray="1 39">
    <line x1="10" y1="13" x2="1190" y2="13"/>
    <line x1="10" y1="307" x2="1190" y2="307"/>
    <line x1="13" y1="10" x2="13" y2="310"/>
    <line x1="1187" y1="10" x2="1187" y2="310"/>
  </g>
  <g stroke="#1e40af" stroke-opacity=".45" fill="none">
    <path d="M30 24v12M24 30h12"/><path d="M1170 24v12M1164 30h12"/>
    <path d="M30 284v12M24 290h12"/><path d="M1170 284v12M1164 290h12"/>
  </g>
  <rect class="scan" x="10" y="10" width="1" height="300" fill="#1e40af" fill-opacity=".12"/>
  <text x="1170" y="42" text-anchor="end" font-size="9.5" letter-spacing="2" fill="#6981b8">SHEET 01 / 04</text>
  <text x="68" y="84" font-size="15" font-weight="700" letter-spacing="5" fill="#2c4d99">TAEHYEONG LIM, PH.D.</text>
  <text x="66" y="152" font-size="50" font-weight="800" letter-spacing="1" fill="#17337a">HUMAN <tspan fill="#dc2626">×</tspan> AI</text>
  <text x="68" y="198" font-size="28" font-weight="700" letter-spacing="3" fill="#17337a">CO-INTELLIGENCE SYSTEMS</text>
  <path d="M68 212h438M68 206v12M506 206v12" fill="none" stroke="#1e40af" stroke-opacity=".5"/>
  <text x="68" y="240" font-size="16" fill="#2c4d99">Building multi-agent systems that think, verify, and work with humans.</text>
  <g font-size="11" font-weight="700" letter-spacing="1" fill="#2c4d99">
    <rect x="68" y="264" width="140" height="30" fill="#1e40af" fill-opacity=".04" stroke="#1e40af" stroke-opacity=".55"/>
    <text x="138" y="283" text-anchor="middle">AI CO-SCIENTIST</text>
    <rect x="218" y="264" width="178" height="30" fill="#1e40af" fill-opacity=".04" stroke="#1e40af" stroke-opacity=".55"/>
    <text x="307" y="283" text-anchor="middle">MULTI-AGENT SYSTEMS</text>
    <rect x="406" y="264" width="164" height="30" fill="#1e40af" fill-opacity=".04" stroke="#1e40af" stroke-opacity=".55"/>
    <text x="488" y="283" text-anchor="middle">HUMAN-IN-THE-LOOP</text>
  </g>
  <g fill="none" stroke="#1e40af">
    <g stroke-opacity=".4" stroke-dasharray="12 4 3 4">
      <path d="M800 140h116M858 82v116"/>
      <path d="M1004 140h116M1062 82v116"/>
    </g>
    <g stroke-opacity=".55" stroke-dasharray="2 5">
      <path d="M858 58v24M1062 58v24"/>
    </g>
    <circle cx="858" cy="53" r="4.5" stroke-opacity=".7"/>
    <circle cx="1062" cy="53" r="4.5" stroke-opacity=".7"/>
    <circle cx="858" cy="140" r="44" stroke-width="2"/>
    <circle cx="1062" cy="140" r="44" stroke-width="2"/>
    <g class="flow" stroke-opacity=".85" stroke-width="1.5">
      <path d="M902 140h45M973 140h45"/>
    </g>
    <circle cx="960" cy="140" r="13" stroke="#dc2626" stroke-width="2"/>
    <g stroke-opacity=".6">
      <path d="M827 109l-20 -20h-54"/>
      <path d="M1093 109l20 -20h54"/>
    </g>
    <g stroke-opacity=".45">
      <path d="M858 188v50M1062 188v50"/>
    </g>
    <g stroke-opacity=".8">
      <path d="M858 232h204"/>
      <path d="M866 228l-8 4 8 4M1054 228l8 4-8 4"/>
    </g>
  </g>
  <text x="749" y="93" text-anchor="end" font-size="10" letter-spacing="1.5" fill="#6981b8">HUMAN INTENT</text>
  <text x="1117" y="93" font-size="10" letter-spacing="1.5" fill="#6981b8">AI AGENCY</text>
  <text x="858" y="145" text-anchor="middle" font-size="11.5" font-weight="800" letter-spacing="1.5" fill="#17337a">HUMAN</text>
  <text x="1062" y="145" text-anchor="middle" font-size="13" font-weight="800" letter-spacing="2" fill="#17337a">AI</text>
  <text x="960" y="145" text-anchor="middle" font-size="15" font-weight="800" fill="#dc2626">×</text>
  <circle class="blink" cx="843" cy="223" r="2.5" fill="#dc2626"/>
  <text x="960" y="226" text-anchor="middle" font-size="9.5" letter-spacing="2" fill="#6981b8">CO-INTELLIGENCE LATTICE / 01</text>
  <g font-size="8.5">
    <rect x="884" y="284" width="306" height="24" fill="none" stroke="#1e40af" stroke-opacity=".5"/>
    <path d="M946 284v24M1086 284v24M1144 284v24" stroke="#1e40af" stroke-opacity=".35"/>
    <text x="915" y="299" text-anchor="middle" font-weight="800" letter-spacing="1" fill="#dc2626">FIG.01</text>
    <text x="1016" y="299" text-anchor="middle" fill="#2c4d99">DWG NO. TL-2026-01</text>
    <text x="1115" y="299" text-anchor="middle" fill="#2c4d99">REV 2026.07</text>
    <text x="1167" y="299" text-anchor="middle" fill="#2c4d99">SCALE 1:1</text>
  </g>
</svg>
```

- [ ] **Step 3: XML 유효성 검증**

Run: `python3 -c "import xml.dom.minidom as m; m.parse('assets/hero-dark.svg'); m.parse('assets/hero-light.svg'); print('OK')"` (repo 루트에서)
Expected: `OK`

- [ ] **Step 4: Commit**

```bash
git add assets/hero-dark.svg assets/hero-light.svg
git commit -m "feat(assets): FIG.01 blueprint hero banner (dark/light)"
```

---

### Task 2: FIG.02 — 아키텍처 다이어그램 SVG 2본

**Files:**
- Create(덮어쓰기): `assets/research-map-dark.svg`
- Create(덮어쓰기): `assets/research-map-light.svg`

**Interfaces:**
- Consumes: 없음
- Produces: README 기존 `<picture>` 태그가 참조하는 동일 파일명 2개 (README 수정 불필요)

유지할 콘텐츠 문자열: `NERV / MAGI`, `AI Co-Scientist`, `orchestrate · verify · remember · act`, 6개 노드 제목·서브텍스트(`Multi-Agent Orchestration/roles · routing · handoffs`, `Tool-Using Agents/actions · APIs · workflows`, `Autonomous Validation/critique · consensus · checks`, `Long-Term Memory/context · retrieval · continuity`, `Human in the Loop/judgment · control · oversight`, `Research Automation/literature · data · writing`), 헤더 `AI SYSTEMS ARCHITECTURE`, `ø45` 주석.

- [ ] **Step 1: `assets/research-map-dark.svg` 작성 (전체 내용 교체)**

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="440" viewBox="0 0 1200 440" role="img" aria-labelledby="title desc">
  <title id="title">AI co-scientist systems architecture</title>
  <desc id="desc">Blueprint schematic: six capability part boxes routed orthogonally to the NERV AI co-scientist core assembly. FIG.02 of 4.</desc>
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#0d2a55"/><stop offset="1" stop-color="#123a75"/>
    </linearGradient>
    <pattern id="gridFine" width="8" height="8" patternUnits="userSpaceOnUse">
      <path d="M8 0H0V8" fill="none" stroke="#ffffff" stroke-opacity=".04"/>
    </pattern>
    <pattern id="gridBold" width="40" height="40" patternUnits="userSpaceOnUse">
      <path d="M40 0H0V40" fill="none" stroke="#ffffff" stroke-opacity=".07"/>
    </pattern>
    <style>
      text { font-family: ui-monospace,'SF Mono',SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace; }
      .flow { stroke-dasharray: 5 7; animation: flow 12s linear infinite; }
      .scan { animation: scan 16s linear infinite; }
      .blink { animation: blink 1.6s steps(1) infinite; }
      @keyframes flow { to { stroke-dashoffset: -96; } }
      @keyframes scan { to { transform: translateX(1180px); } }
      @keyframes blink { 0%, 49% { opacity: 1; } 50%, 100% { opacity: .12; } }
      @media (prefers-reduced-motion: reduce) { .flow, .scan, .blink { animation: none; } }
    </style>
  </defs>
  <rect width="1200" height="440" fill="url(#bg)"/>
  <rect width="1200" height="440" fill="url(#gridFine)"/>
  <rect width="1200" height="440" fill="url(#gridBold)"/>
  <rect x="2" y="2" width="1196" height="436" fill="none" stroke="#dbeafe" stroke-opacity=".6" stroke-width="2.5"/>
  <rect x="10" y="10" width="1180" height="420" fill="none" stroke="#dbeafe" stroke-opacity=".28"/>
  <g stroke="#dbeafe" stroke-opacity=".3" stroke-width="6" stroke-dasharray="1 39">
    <line x1="10" y1="13" x2="1190" y2="13"/>
    <line x1="10" y1="427" x2="1190" y2="427"/>
    <line x1="13" y1="10" x2="13" y2="430"/>
    <line x1="1187" y1="10" x2="1187" y2="430"/>
  </g>
  <g stroke="#dbeafe" stroke-opacity=".45" fill="none">
    <path d="M30 24v12M24 30h12"/><path d="M1170 24v12M1164 30h12"/>
    <path d="M30 404v12M24 410h12"/><path d="M1170 404v12M1164 410h12"/>
  </g>
  <rect class="scan" x="10" y="10" width="1" height="420" fill="#dbeafe" fill-opacity=".16"/>
  <text x="54" y="54" font-size="14" font-weight="700" letter-spacing="3" fill="#b9d0f0">AI SYSTEMS ARCHITECTURE</text>
  <text x="1170" y="42" text-anchor="end" font-size="9.5" letter-spacing="2" fill="#8fb0dd">SHEET 02 / 04</text>
  <g fill="none">
    <g class="flow" stroke="#dbeafe" stroke-opacity=".7" stroke-width="1.5">
      <path d="M370 116H410V216H450"/>
      <path d="M600 128V182"/>
      <path d="M370 350H410V264H450"/>
      <path d="M600 352V298"/>
    </g>
    <path d="M830 116H790V216H750" stroke="#dbeafe" stroke-opacity=".7" stroke-width="1.5" stroke-dasharray="4 5"/>
    <path d="M830 350H790V264H750" stroke="#f87171" stroke-opacity=".8" stroke-width="1.5" stroke-dasharray="4 5"/>
  </g>
  <g fill="#dbeafe" fill-opacity=".9">
    <circle cx="410" cy="116" r="2"/><circle cx="410" cy="216" r="2"/>
    <circle cx="410" cy="350" r="2"/><circle cx="410" cy="264" r="2"/>
    <circle cx="790" cy="116" r="2"/><circle cx="790" cy="216" r="2"/>
  </g>
  <g fill="#f87171" fill-opacity=".9">
    <circle cx="790" cy="350" r="2"/><circle cx="790" cy="264" r="2"/>
  </g>
  <rect x="450" y="182" width="300" height="116" fill="#dbeafe" fill-opacity=".05" stroke="#dbeafe" stroke-opacity=".85" stroke-width="2"/>
  <rect x="456" y="188" width="288" height="104" fill="none" stroke="#dbeafe" stroke-opacity=".35"/>
  <text x="600" y="214" text-anchor="middle" font-size="12" font-weight="700" letter-spacing="3" fill="#b9d0f0">NERV / MAGI</text>
  <text x="600" y="246" text-anchor="middle" font-size="22" font-weight="800" fill="#eaf2ff">AI Co-Scientist</text>
  <text x="600" y="272" text-anchor="middle" font-size="12" fill="#b9d0f0">orchestrate · verify · remember · act</text>
  <g fill="none" stroke="#f87171" stroke-opacity=".8">
    <path d="M750 182l28 -24h70"/>
  </g>
  <text x="854" y="162" font-size="11" font-weight="700" letter-spacing="1" fill="#f87171">ø45 AGENTS</text>
  <g font-size="9" font-weight="800" letter-spacing="1">
    <g fill="none" stroke="#dbeafe" stroke-opacity=".7">
      <rect x="120" y="84" width="250" height="64" fill="#dbeafe" fill-opacity=".04"/>
      <rect x="120" y="74" width="46" height="16"/>
      <rect x="475" y="64" width="250" height="64" fill="#dbeafe" fill-opacity=".04"/>
      <rect x="475" y="54" width="46" height="16"/>
      <rect x="830" y="84" width="250" height="64" fill="#dbeafe" fill-opacity=".04"/>
      <rect x="830" y="74" width="46" height="16"/>
      <rect x="120" y="318" width="250" height="64" fill="#dbeafe" fill-opacity=".04"/>
      <rect x="120" y="308" width="46" height="16"/>
      <rect x="475" y="352" width="250" height="64" fill="#dbeafe" fill-opacity=".04"/>
      <rect x="475" y="342" width="46" height="16"/>
    </g>
    <g fill="none" stroke="#f87171" stroke-opacity=".9">
      <rect x="830" y="318" width="250" height="64" fill="#f87171" fill-opacity=".05"/>
      <rect x="830" y="308" width="46" height="16"/>
    </g>
    <text x="143" y="86" text-anchor="middle" fill="#b9d0f0">PT-01</text>
    <text x="498" y="66" text-anchor="middle" fill="#b9d0f0">PT-02</text>
    <text x="853" y="86" text-anchor="middle" fill="#b9d0f0">PT-03</text>
    <text x="143" y="320" text-anchor="middle" fill="#b9d0f0">PT-04</text>
    <text x="853" y="320" text-anchor="middle" fill="#f87171">PT-05</text>
    <text x="498" y="354" text-anchor="middle" fill="#b9d0f0">PT-06</text>
  </g>
  <g font-size="14.5" font-weight="700" fill="#eaf2ff">
    <text x="136" y="112">Multi-Agent Orchestration</text>
    <text x="491" y="92">Tool-Using Agents</text>
    <text x="846" y="112">Autonomous Validation</text>
    <text x="136" y="346">Long-Term Memory</text>
    <text x="846" y="346">Human in the Loop</text>
    <text x="491" y="380">Research Automation</text>
  </g>
  <g font-size="11" fill="#8fb0dd">
    <text x="136" y="134">roles · routing · handoffs</text>
    <text x="491" y="114">actions · APIs · workflows</text>
    <text x="846" y="134">critique · consensus · checks</text>
    <text x="136" y="368">context · retrieval · continuity</text>
    <text x="846" y="368">judgment · control · oversight</text>
    <text x="491" y="402">literature · data · writing</text>
  </g>
  <circle class="blink" cx="1062" cy="350" r="3" fill="#f87171"/>
  <g font-size="9" letter-spacing="1" fill="#8fb0dd">
    <path d="M54 410h30" stroke="#dbeafe" stroke-opacity=".85" stroke-width="1.5" fill="none"/>
    <text x="92" y="413">COMMAND FLOW</text>
    <path d="M54 424h30" stroke="#dbeafe" stroke-opacity=".85" stroke-width="1.5" stroke-dasharray="4 5" fill="none"/>
    <text x="92" y="427">VALIDATION FEEDBACK</text>
  </g>
  <g font-size="8.5">
    <rect x="884" y="404" width="306" height="24" fill="none" stroke="#dbeafe" stroke-opacity=".5"/>
    <path d="M946 404v24M1086 404v24M1144 404v24" stroke="#dbeafe" stroke-opacity=".35"/>
    <text x="915" y="419" text-anchor="middle" font-weight="800" letter-spacing="1" fill="#f87171">FIG.02</text>
    <text x="1016" y="419" text-anchor="middle" fill="#b9d0f0">DWG NO. TL-2026-02</text>
    <text x="1115" y="419" text-anchor="middle" fill="#b9d0f0">REV 2026.07</text>
    <text x="1167" y="419" text-anchor="middle" fill="#b9d0f0">SCALE 1:1</text>
  </g>
</svg>
```

- [ ] **Step 2: `assets/research-map-light.svg` 작성 (전체 내용 교체)**

다크본과 동일 지오메트리에 아래 치환만 적용한 완전한 파일을 작성한다 (Task 1 Step 2에서 실제 예시를 볼 수 있듯 요소 구조는 그대로):
`#0d2a55→#ffffff`, `#123a75→#f3f7fd`, 모눈 `#ffffff/.04/.07→#1e40af/.06/.09`, `#dbeafe→#1e40af`(프레임 .6→.55, 내부선 .28→.25), `#eaf2ff→#17337a`, `#b9d0f0→#2c4d99`, `#8fb0dd→#6981b8`, `#f87171→#dc2626`, 스캔라인 fill-opacity `.16→.12`, `<desc>`를 `Whiteprint schematic: ...` 으로. 그 외 좌표·텍스트·클래스는 모두 동일.

- [ ] **Step 3: XML 유효성 검증**

Run: `python3 -c "import xml.dom.minidom as m; m.parse('assets/research-map-dark.svg'); m.parse('assets/research-map-light.svg'); print('OK')"`
Expected: `OK`

- [ ] **Step 4: Commit**

```bash
git add assets/research-map-dark.svg assets/research-map-light.svg
git commit -m "feat(assets): FIG.02 blueprint architecture schematic (dark/light)"
```

---

### Task 3: FIG.03 — NERV 카드 2본 + README 반영

**Files:**
- Create: `assets/project-nerv-dark.svg`
- Create: `assets/project-nerv-light.svg`
- Delete: `assets/project-nerv.svg`
- Modify: `README.md:29` (단일 img → picture 태그)

**Interfaces:**
- Consumes: 없음
- Produces: README가 참조할 신규 파일명 `project-nerv-dark.svg` / `project-nerv-light.svg`

유지할 콘텐츠 문자열: `AI CO-SCIENTIST SYSTEM`, `NERV`, `SYSTEM WHITEPAPER`, `A 45-agent AI co-scientist for complex research workflows.`, `Role-based agents · autonomous cross-validation · research workflow orchestration`, `45 AI AGENTS`, `7 SYSTEM ROLES`, `MAGI VALIDATION`, `RESEARCH`/`CORE`, `READ THE WHITEPAPER →`.

- [ ] **Step 1: `assets/project-nerv-dark.svg` 작성**

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="270" viewBox="0 0 1200 270" role="img" aria-labelledby="title desc">
  <title id="title">NERV System Whitepaper</title>
  <desc id="desc">Blueprint card for NERV, a 45-agent AI co-scientist system, with MAGI validation stamp. FIG.03 of 4.</desc>
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#0d2a55"/><stop offset="1" stop-color="#123a75"/>
    </linearGradient>
    <pattern id="gridFine" width="8" height="8" patternUnits="userSpaceOnUse">
      <path d="M8 0H0V8" fill="none" stroke="#ffffff" stroke-opacity=".04"/>
    </pattern>
    <pattern id="gridBold" width="40" height="40" patternUnits="userSpaceOnUse">
      <path d="M40 0H0V40" fill="none" stroke="#ffffff" stroke-opacity=".07"/>
    </pattern>
    <style>
      text { font-family: ui-monospace,'SF Mono',SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace; }
      .flow { stroke-dasharray: 5 7; animation: flow 12s linear infinite; }
      .scan { animation: scan 16s linear infinite; }
      .blink { animation: blink 1.6s steps(1) infinite; }
      @keyframes flow { to { stroke-dashoffset: -96; } }
      @keyframes scan { to { transform: translateX(1180px); } }
      @keyframes blink { 0%, 49% { opacity: 1; } 50%, 100% { opacity: .12; } }
      @media (prefers-reduced-motion: reduce) { .flow, .scan, .blink { animation: none; } }
    </style>
  </defs>
  <rect width="1200" height="270" fill="url(#bg)"/>
  <rect width="1200" height="270" fill="url(#gridFine)"/>
  <rect width="1200" height="270" fill="url(#gridBold)"/>
  <rect x="2" y="2" width="1196" height="266" fill="none" stroke="#dbeafe" stroke-opacity=".6" stroke-width="2.5"/>
  <rect x="10" y="10" width="1180" height="250" fill="none" stroke="#dbeafe" stroke-opacity=".28"/>
  <g stroke="#dbeafe" stroke-opacity=".3" stroke-width="6" stroke-dasharray="1 39">
    <line x1="10" y1="13" x2="1190" y2="13"/>
    <line x1="10" y1="257" x2="1190" y2="257"/>
    <line x1="13" y1="10" x2="13" y2="260"/>
    <line x1="1187" y1="10" x2="1187" y2="260"/>
  </g>
  <rect class="scan" x="10" y="10" width="1" height="250" fill="#dbeafe" fill-opacity=".16"/>
  <text x="1170" y="40" text-anchor="end" font-size="9.5" letter-spacing="2" fill="#8fb0dd">SHEET 03 / 04</text>
  <path d="M46 40V230" stroke="#f87171" stroke-width="3"/>
  <path d="M42 40h8M42 230h8" stroke="#f87171" stroke-width="1.5"/>
  <text x="72" y="72" font-size="13" font-weight="800" letter-spacing="3" fill="#f87171">AI CO-SCIENTIST SYSTEM</text>
  <text x="72" y="122" font-size="44" font-weight="900" fill="#eaf2ff">NERV<tspan dx="16" font-size="21" font-weight="700" fill="#b9d0f0">SYSTEM WHITEPAPER</tspan></text>
  <text x="74" y="156" font-size="16.5" fill="#b9d0f0">A 45-agent AI co-scientist for complex research workflows.</text>
  <text x="74" y="182" font-size="12.5" fill="#8fb0dd">Role-based agents · autonomous cross-validation · research workflow orchestration</text>
  <g font-size="11" font-weight="700" letter-spacing="1">
    <rect x="74" y="204" width="132" height="28" fill="#f87171" fill-opacity=".07" stroke="#f87171" stroke-opacity=".7"/>
    <text x="140" y="222" text-anchor="middle" fill="#f87171">45 AI AGENTS</text>
    <rect x="216" y="204" width="150" height="28" fill="#dbeafe" fill-opacity=".05" stroke="#dbeafe" stroke-opacity=".55"/>
    <text x="291" y="222" text-anchor="middle" fill="#b9d0f0">7 SYSTEM ROLES</text>
    <rect x="376" y="204" width="164" height="28" fill="#dbeafe" fill-opacity=".05" stroke="#dbeafe" stroke-opacity=".55"/>
    <text x="458" y="222" text-anchor="middle" fill="#b9d0f0">MAGI VALIDATION</text>
  </g>
  <g fill="none" stroke="#dbeafe">
    <circle cx="940" cy="136" r="94" stroke-opacity=".18" stroke-dasharray="4 8"/>
    <g class="flow" stroke-opacity=".6">
      <path d="M940 104V66"/>
      <path d="M965 116L995 92"/>
      <path d="M971 143L1008 152"/>
      <path d="M954 165L970 199"/>
      <path d="M926 165L910 199"/>
      <path d="M909 143L872 152"/>
      <path d="M915 116L885 92"/>
    </g>
    <circle cx="940" cy="136" r="32" stroke-width="2"/>
    <g stroke-opacity=".8">
      <circle cx="940" cy="58" r="8"/>
      <circle cx="1001" cy="87" r="8"/>
      <circle cx="1016" cy="153" r="8"/>
      <circle cx="974" cy="206" r="8"/>
      <circle cx="906" cy="206" r="8"/>
      <circle cx="864" cy="153" r="8"/>
      <circle cx="879" cy="87" r="8"/>
    </g>
    <path d="M856 153H800" stroke="#f87171" stroke-opacity=".8"/>
  </g>
  <text x="940" y="132" text-anchor="middle" font-size="10.5" font-weight="800" letter-spacing="1" fill="#eaf2ff">RESEARCH</text>
  <text x="940" y="146" text-anchor="middle" font-size="9" letter-spacing="1" fill="#8fb0dd">CORE</text>
  <text x="796" y="157" text-anchor="end" font-size="10.5" font-weight="700" letter-spacing="1" fill="#f87171">ø 7 ROLES</text>
  <g transform="translate(1092 58) rotate(-8)" opacity=".92">
    <rect x="-78" y="-26" width="156" height="52" rx="6" fill="none" stroke="#f87171" stroke-width="2.5"/>
    <rect x="-72" y="-20" width="144" height="40" rx="4" fill="none" stroke="#f87171" stroke-opacity=".5"/>
    <text x="0" y="-2" text-anchor="middle" font-size="17" font-weight="900" letter-spacing="4" fill="#f87171">MAGI</text>
    <text x="0" y="14" text-anchor="middle" font-size="10" letter-spacing="3" fill="#f87171">VALIDATED</text>
  </g>
  <text x="1160" y="228" text-anchor="end" font-size="11.5" font-weight="800" letter-spacing="1" fill="#eaf2ff">READ THE WHITEPAPER <tspan fill="#f87171">→</tspan></text>
  <g font-size="8.5">
    <rect x="560" y="234" width="306" height="24" fill="none" stroke="#dbeafe" stroke-opacity=".5"/>
    <path d="M622 234v24M762 234v24M820 234v24" stroke="#dbeafe" stroke-opacity=".35"/>
    <text x="591" y="249" text-anchor="middle" font-weight="800" letter-spacing="1" fill="#f87171">FIG.03</text>
    <text x="692" y="249" text-anchor="middle" fill="#b9d0f0">DWG NO. TL-2026-03</text>
    <text x="791" y="249" text-anchor="middle" fill="#b9d0f0">REV 2026.07</text>
    <text x="843" y="249" text-anchor="middle" fill="#b9d0f0">SCALE 1:1</text>
  </g>
</svg>
```

주의: 타이틀 블록은 우하단의 `READ THE WHITEPAPER →`와 겹치지 않도록 x=560(중앙 하단)에 배치했다.

- [ ] **Step 2: `assets/project-nerv-light.svg` 작성**

다크본과 동일 지오메트리에 Global Constraints의 라이트 팔레트 치환(`#0d2a55→#ffffff`, `#123a75→#f3f7fd`, 모눈 `#ffffff/.04/.07→#1e40af/.06/.09`, `#dbeafe→#1e40af`, `#eaf2ff→#17337a`, `#b9d0f0→#2c4d99`, `#8fb0dd→#6981b8`, `#f87171→#dc2626`, 스캔 `.16→.12`)을 적용한 완전한 파일. `<desc>`는 `Whiteprint card for NERV...`로.

- [ ] **Step 3: 기존 단일본 삭제 + README 수정**

```bash
git rm assets/project-nerv.svg
```

`README.md`의 아래 줄(현재 29행)을:

```html
<a href="https://taehyeonglim.github.io/nerv-whitepaper/"><img src="https://raw.githubusercontent.com/taehyeonglim/taehyeonglim/main/assets/project-nerv.svg" alt="NERV System Whitepaper — a 45-agent AI co-scientist system" width="100%"></a>
```

다음으로 교체:

```html
<a href="https://taehyeonglim.github.io/nerv-whitepaper/">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/taehyeonglim/taehyeonglim/main/assets/project-nerv-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/taehyeonglim/taehyeonglim/main/assets/project-nerv-light.svg">
    <img alt="NERV System Whitepaper — a 45-agent AI co-scientist system" src="https://raw.githubusercontent.com/taehyeonglim/taehyeonglim/main/assets/project-nerv-light.svg" width="100%">
  </picture>
</a>
```

- [ ] **Step 4: XML 유효성 검증**

Run: `python3 -c "import xml.dom.minidom as m; m.parse('assets/project-nerv-dark.svg'); m.parse('assets/project-nerv-light.svg'); print('OK')"`
Expected: `OK`

- [ ] **Step 5: Commit**

```bash
git add assets/project-nerv-dark.svg assets/project-nerv-light.svg README.md
git commit -m "feat(assets): FIG.03 blueprint NERV card with light variant"
```

---

### Task 4: FIG.04 — 액티비티 차트 생성 스크립트 (TDD)

**Files:**
- Create: `scripts/generate_activity.py`
- Test: `tests/test_generate_activity.py`

**Interfaces:**
- Consumes: 없음
- Produces: CLI `python3 scripts/generate_activity.py --user <login> --out <dir> [--fixture <json>]` → `<dir>/build-activity-dark.svg`, `<dir>/build-activity.svg`. 함수 `weekly_series(calendar) -> (list[tuple[str,int]], int)`, `render_svg(weeks, total, palette) -> str`, `PALETTES: dict`.

- [ ] **Step 1: 실패하는 테스트 작성 — `tests/test_generate_activity.py`**

```python
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
```

- [ ] **Step 2: 테스트가 실패하는지 확인**

Run: `python3 -m unittest tests.test_generate_activity -v` (repo 루트에서)
Expected: FAIL — `ModuleNotFoundError: No module named 'generate_activity'`

- [ ] **Step 3: `scripts/generate_activity.py` 구현**

```python
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
```

- [ ] **Step 4: 테스트 통과 확인**

Run: `python3 -m unittest tests.test_generate_activity -v`
Expected: 전부 PASS (7 tests OK)

- [ ] **Step 5: 실데이터 스모크 테스트 (로컬)**

Run: `GITHUB_TOKEN=$(gh auth token) python3 scripts/generate_activity.py --user taehyeonglim --out /tmp/blueprint-activity && python3 -c "import xml.dom.minidom as m; m.parse('/tmp/blueprint-activity/build-activity-dark.svg'); print('OK')"`
Expected: `wrote ...` 2줄 + `OK`

- [ ] **Step 6: Commit**

```bash
git add scripts/generate_activity.py tests/test_generate_activity.py
git commit -m "feat(activity): blueprint FIG.04 chart generator with tests"
```

---

### Task 5: 워크플로 교체 + README 액티비티 섹션 반영

**Files:**
- Create: `.github/workflows/blueprint-activity.yml`
- Delete: `.github/workflows/snake.yml`
- Modify: `README.md:56-64` (액티비티 섹션)

**Interfaces:**
- Consumes: Task 4의 CLI (`scripts/generate_activity.py --user taehyeonglim --out dist`)
- Produces: output 브랜치의 `build-activity-dark.svg` / `build-activity.svg`

- [ ] **Step 1: `.github/workflows/blueprint-activity.yml` 작성**

```yaml
name: Generate Blueprint Activity

on:
  schedule:
    - cron: "0 */12 * * *"
  workflow_dispatch:
  push:
    branches:
      - main

permissions:
  contents: write

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Generate activity SVGs
        run: python3 scripts/generate_activity.py --user taehyeonglim --out dist
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

      - name: Push to output branch
        uses: crazy-max/ghaction-github-pages@v4
        with:
          target_branch: output
          build_dir: dist
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

- [ ] **Step 2: `snake.yml` 삭제**

```bash
git rm .github/workflows/snake.yml
```

- [ ] **Step 3: README 액티비티 섹션 교체**

`README.md`의 `## AI systems build activity` 아래 `<div align="center">` 안에서, activity-graph 링크 줄과 스네이크 `<picture>` 블록(현재 58~64행):

```html
[![AI Systems Build Activity](https://github-readme-activity-graph.vercel.app/graph?username=taehyeonglim&theme=tokyo-night&hide_border=true&area=true&custom_title=AI%20Systems%20Build%20Activity)](https://github.com/ashutosh00710/github-readme-activity-graph)

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/taehyeonglim/taehyeonglim/output/github-contribution-grid-snake-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/taehyeonglim/taehyeonglim/output/github-contribution-grid-snake.svg">
  <img alt="Contribution snake animation" src="https://raw.githubusercontent.com/taehyeonglim/taehyeonglim/output/github-contribution-grid-snake.svg">
</picture>
```

을 아래로 교체:

```html
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/taehyeonglim/taehyeonglim/output/build-activity-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/taehyeonglim/taehyeonglim/output/build-activity.svg">
  <img alt="Blueprint-style weekly build activity chart" src="https://raw.githubusercontent.com/taehyeonglim/taehyeonglim/output/build-activity.svg" width="100%">
</picture>
```

- [ ] **Step 4: 워크플로 문법 검증**

Run: `python3 -c "import yaml,sys; yaml.safe_load(open('.github/workflows/blueprint-activity.yml')); print('OK')"` — PyYAML이 없으면 `ruby -ryaml -e "YAML.load_file('.github/workflows/blueprint-activity.yml'); puts 'OK'"` (macOS 기본 ruby)
Expected: `OK`

- [ ] **Step 5: Commit**

```bash
git add .github/workflows/blueprint-activity.yml README.md
git commit -m "feat(activity): replace external graph and snake with blueprint FIG.04 workflow"
```

---

### Task 6: 시각 QA + 사용자 승인 게이트 + 배포

**Files:**
- Create(스크래치패드, repo 외부): `preview.html` — 4개 에셋(다크/라이트)을 한 화면에 나열하는 검수용 갤러리

**Interfaces:**
- Consumes: Task 1~5의 모든 산출물
- Produces: main 병합 + push (사용자 승인 후에만)

- [ ] **Step 1: 검수 갤러리 작성 (스크래치패드 디렉토리에)**

```html
<!doctype html><meta charset="utf-8"><title>Blueprint preview</title>
<style>body{margin:0;font-family:monospace}section{padding:24px}
.dark{background:#0d1117}.light{background:#ffffff}
img{width:100%;max-width:1200px;display:block;margin:0 auto 16px}</style>
<section class="dark">
  <img src="REPO/assets/hero-dark.svg"><img src="REPO/assets/research-map-dark.svg">
  <img src="REPO/assets/project-nerv-dark.svg"><img src="ACT/build-activity-dark.svg">
</section>
<section class="light">
  <img src="REPO/assets/hero-light.svg"><img src="REPO/assets/research-map-light.svg">
  <img src="REPO/assets/project-nerv-light.svg"><img src="ACT/build-activity.svg">
</section>
```

`REPO`는 `file:///Users/taehyeong/Documents/GitHub/taehyeonglim` 절대경로로, `ACT`는 Task 4 Step 5의 `/tmp/blueprint-activity` 경로로 치환. file:// 접근이 막히면 repo 루트에서 `python3 -m http.server 8901`을 배경 실행하고 `http://localhost:8901/` 기준 상대경로 사용.

- [ ] **Step 2: 브라우저 렌더 확인 및 스크린샷**

Chrome 도구로 preview.html을 열어 8장 전부 스크린샷 → 텍스트 겹침·클리핑·좌표 오차를 발견하면 해당 SVG 좌표를 수정하고 재확인 (수정 시 해당 Task 브랜치 커밋에 fixup 커밋 추가).

- [ ] **Step 3: 사용자 시안 승인 게이트 (STOP)**

스크린샷을 사용자에게 제시하고 승인을 받는다. **승인 전에는 main 병합·push 금지.** 수정 요청이 있으면 반영 후 재확인.

- [ ] **Step 4: (승인 후) main 병합 + push**

```bash
git checkout main && git merge --no-ff redesign/blueprint -m "feat: blueprint profile redesign (FIG.01-04)"
git push origin main
```

- [ ] **Step 5: 워크플로 실행 확인**

push가 `Generate Blueprint Activity`를 트리거한다. 확인:
`gh run watch --repo taehyeonglim/taehyeonglim $(gh run list --repo taehyeonglim/taehyeonglim --workflow=blueprint-activity.yml --limit 1 --json databaseId -q '.[0].databaseId')`
Expected: `✓ ... completed with 'success'` 후 output 브랜치에 `build-activity-dark.svg`/`build-activity.svg` 존재 (`gh api repos/taehyeonglim/taehyeonglim/contents/?ref=output`)

- [ ] **Step 6: 라이브 프로필 확인**

브라우저로 `https://github.com/taehyeonglim` 접속, 4개 에셋 렌더 확인 (camo 캐시로 수 분 지연 가능 — 쿼리스트링 `?v=2` 없이 대기가 원칙). 라이트/다크 각각 확인.

---

## Self-Review 결과

- 스펙 커버리지: FIG.01(Task 1), FIG.02(Task 2), FIG.03+README(Task 3), FIG.04 스크립트(Task 4), 워크플로+README(Task 5), 검증·승인·배포(Task 6) — 스펙 §3~§7 전 항목 매핑 완료. §6 에러 처리는 Task 4 Step 3의 `fetch_calendar` RuntimeError(→ Action 실패 → output 미갱신)로 구현.
- 플레이스홀더: 라이트 변형 2건(Task 2/3의 Step 2)은 치환 규칙 + Task 1의 완전한 실물 예시로 명세 — 치환표가 결정적(deterministic)이므로 허용. 그 외 전체 코드 포함.
- 타입 일관성: `weekly_series`/`render_svg`/`PALETTES` 시그니처가 Task 4 테스트·구현·Task 5 CLI 호출에서 일치. output 파일명 `build-activity-dark.svg`/`build-activity.svg`가 Task 4/5/README에서 일치.
