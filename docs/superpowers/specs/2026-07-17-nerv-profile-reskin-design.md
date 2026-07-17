# GitHub 프로필 NERV 리스킨 — 디자인 스펙

- 날짜: 2026-07-17
- 대상 저장소: `taehyeonglim/taehyeonglim` (GitHub 프로필 README)
- 범위: 전체 SVG 자산 8쌍 — 히어로 / 버튼 3종 / 연구 지도 / NERV 카드 / 필드 리절트 / 빌드 액티비티
- 선행 스펙: `2026-07-13-blueprint-profile-redesign-design.md` (파이프라인·검증 골격 계승)

## 1. 목표

블루프린트(제도 도면) 테마를 **NERV 테마**로 전면 리스킨한다. 프로필의 콘텐츠는 이미 전부 NERV 이야기이므로, 클릭 목적지인 whitepaper·대시보드와 시각 세계관을 통일해 프로필을 NERV 시스템의 관문으로 만든다. 각 자산의 콘텐츠(문구·정보 구성·링크)는 유지하고 스킨만 교체한다.

**컨셉 한 줄** — 다크 모드는 *MAGI 터미널에 떠 있는 시스템 화면*, 라이트 모드는 *NERV 본부가 발행한 공문서 인쇄본*. 같은 정보를 두 세계관 매체로 보여준다.

**확정된 결정**

| 결정 항목 | 선택 |
|---|---|
| 컨셉 | 다크 = MAGI 터미널 / 라이트 = NERV 공문서 인쇄본 |
| 플레이버 강도 | 중간 — whitepaper 기조 + MAGI 터미널 장치. 일본어는 히어로 서브라벨 1곳만 |
| 접근 | 인플레이스 리스킨 — 파일명·README 마크업·FIG 연번·output 브랜치 전부 불변 |
| 팔레트 배분 | FIG.01~04 + 버튼 = NERV 레드 기조 / FIG.05 = 다크에서만 MAGI 앰버 기조 |
| 모션 | 다크만 (스캔라인 1 + 마커 blink) / 라이트는 완전 정적 (인쇄물 컨셉) |
| 타이포 | 대형 디스플레이만 Chakra Petch 패스 아웃라인 임베드, 라벨·본문은 시스템 모노 스택 |

**레퍼런스 (팔레트·어휘의 출처, SSOT)**

- whitepaper: `~/nerv-whitepaper/site/assets/nerv.css` — 레드/아이보리/블랙, 컷코너, 택티컬 그리드
- 대시보드: `~/NERV/Agents/Lab Director/project-dashboard/static/magi/magi-tokens.css` + `design-reference/magi-terminal-hero.html` — 보이드/앰버/오렌지, 스캔라인, 브래킷 라벨

## 2. 공통 디자인 시스템 "NERV/MAGI"

### 색상

| 역할 | 다크 (MAGI 터미널) | 라이트 (NERV 공문서) |
|---|---|---|
| 바탕 | 보이드 `#050609 → #0a0c12` 그라데이션 + 상단 레드 radial 글로우 `rgba(217,39,32,.11)` | 아이보리 종이 `#f4efe6` + 미세 음영 `#ece5d8` |
| 잉크 | 제목 `#f4efe6` / 본문 `#d8d5ce` / muted `#8d9098` / dim `#5c6069` | 먹색 제목 `#1a1b1e` / 본문 `#2a2b30` / muted `#6b6558` |
| 주 강조 | NERV 레드 `#ff3b30` (밝음) · `#d92720` (기본) · `#780f10` (딥) | 레드 스탬프/인주 `#d92720` |
| 보조 | MAGI 앰버 `#ffb000` (FIG.05·상태), OK 그린 `#34d399` (텔레메트리) | 없음 — 먹 + 레드 2색 인쇄 원칙 |
| 그리드 | 옅은 아이보리 이중 그리드 (8px 세밀 `rgba(244,239,230,.03)` + 40px 굵음 `.05`) + 레드 축선 `rgba(255,59,48,.16)` | 옅은 잉크 괘선 `rgba(26,27,30,.08~.12)` |

- 그리드의 8px+40px 이중 구조는 블루프린트에서 계승 (검증된 밀도), 색만 교체.
- 앰버·그린은 다크 전용. 라이트는 공문서 컨셉에 따라 먹+레드 2색만 쓴다.

### 타이포그래피

- 라벨·본문: `ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, "Liberation Mono", monospace` (기존 유지). 대문자 + 넓은 자간(0.1~0.2em) 원칙 유지.
- 대형 디스플레이 타이포(히어로 메인 타이틀, FIG.03 카드 타이틀)만 **Chakra Petch → SVG 패스 아웃라인 변환** 후 임베드. GitHub `<img>` SVG는 외부 폰트 로드가 불가능하므로 패스가 유일한 충실 재현 수단. 변환은 로컬 fonttools로 1회 수행(장당 +수 KB). 변환이 품질 미달이면 폴백: 시스템 모노 대문자 + 자간 압축.

### 공통 어휘 (전 자산)

- **컷코너 패널**: `clip-path` 대각 컷 14px (FIG.03 대형 카드만 32px) — whitepaper 문법.
- **브래킷 라벨**: `[ P-01 ]` 식 — 대시보드 문법. 기존 파트넘버 표기를 이 형태로 리스킨.
- **NERV 문서 헤더** (기존 도곽 타이틀 블록의 리스킨): `FIG.NN / DOC NO. NERV-TL-2026-NN / REV 2026.07 / STATUS: MAGI CHECKED`. FIG 연번 5장 체계는 그대로 유지.
- **스탬프**: 라이트 모드에서 레드 스탬프(살짝 기울임)를 승인 장치로 사용. 다크에서는 레드 글로우 배지로 대응.
- **일본어**: 히어로 서브라벨 1곳만 — `協働知能システム`. 그 외 자산에는 넣지 않는다.
- **원작 로고 금지**: NERV 반잎 로고 등 원작 도형은 사용하지 않는다 (기존 방침 유지).

### 모션

- 다크: 가는 스캔라인 1개 + 포인트 마커 blink. 전부 SVG 내부 CSS `@keyframes`, `prefers-reduced-motion: reduce`에서 전체 정지. CRT 전면 오버레이·부팅 시퀀스는 채택하지 않는다 (README 스케일에서 과함).
- 라이트: 모션 0. 인쇄물이라는 컨셉이 정적의 이유가 된다.

## 3. 자산별 설계 (콘텐츠 문구 전부 유지)

### FIG.01 — 히어로 (1200×320, `hero-dark.svg` / `hero-light.svg` 교체)

- 다크: 상단 터미널 스테이터스 라인 `SYSTEM NOMINAL · 45 AGENTS ACTIVE` (그린 dot + 모노 라벨). 좌측 타이포 블록 문구 유지 — eyebrow `TAEHYEONG LIM, PH.D.`, 메인 `HUMAN × AI` / `CO-INTELLIGENCE SYSTEMS` (Chakra Petch 패스, `×`만 레드), 서브 문구 유지, 일본어 서브라벨 `協働知能システム` 1곳. 캡슐 3개는 컷코너 라벨로. 우측 크로스헤어 래티스(HUMAN INTENT / AI AGENCY)는 HUD 레티클 문법으로 리스킨. 스캔라인 1개.
- 라이트: 공문서 표지 — 상단 레터헤드(발행 기관 표기 스타일), 레드 등록선, 우하단 NERV 문서 헤더 + 레드 스탬프.

### 버튼 3종 (148/172×34, `btn-whitepaper` / `btn-agents` / `btn-magi` 각 dark/light 교체)

- 컷코너 캡슐(작은 컷 6~8px). 다크 = 레드 아웃라인 + 은은한 글로우, 라이트 = 먹 잉크 테두리 + 레드 포인트. 문구·링크 유지.

### FIG.02 — 연구 지도 (1200×440, `research-map-dark.svg` / `-light.svg` 교체)

- 직교 배선(90° 꺾임), 허브-스포크 구성, `PT-01`~`PT-06` 파트넘버, 실선/점선 범례 전부 유지. 부품 박스를 컷코너 모듈 카드로, 파트넘버를 브래킷 라벨 `[ PT-01 ]`로 리스킨.
- **HITL 박스 레드 강조 유지** — "인간 최종 통제"는 NERV 테마에서 더 자연스러운 레드의 자리.

### FIG.03 — NERV 카드 (1200×270, `project-nerv-dark.svg` / `-light.svg` 교체)

- 클릭 목적지(whitepaper)와 시각 연속성이 가장 중요한 카드. whitepaper 랜딩 히어로를 미러링: eyebrow `NERV TECHNICAL WHITEPAPER`, 32px 컷코너 패널, 방사형 7노드·캡슐 3개·`READ THE WHITEPAPER →` 문구 유지.
- `MAGI VALIDATED` 스탬프 유지 (다크 = 글로우 배지, 라이트 = 레드 스탬프).

### FIG.04 — 필드 리절트 (1200×200, `field-results-dark.svg` / `-light.svg` 교체)

- 다크 = 게재 실적 터미널 readout, 라이트 = 게재 증명 공문서. 서지 정보·DOI 링크 유지.
- **행 추가가 쉬운 테이블 구조 유지** — 2026년 8월 게재 예정 논문(R-02) 추가가 예약되어 있다.

### FIG.05 — 빌드 액티비티 차트 (1200×340, `scripts/generate_activity.py` 산출)

- `PALETTES` dict에서 기존 blueprint 키를 NERV 팔레트로 교체: 다크 = 보이드 배경 + **앰버/오렌지 막대** (`#ffb000`/`#ff6a00`) + 레드 피크 콜아웃, 라이트 = 종이 배경 + 먹 잉크 막대 + 레드 피크 콜아웃.
- 유일하게 앰버 기조를 쓰는 자산 — "살아있는 계기판"으로서 MAGI 모니터 문법을 따른다.
- 렌더 템플릿의 도곽·타이틀 블록도 §2 공통 어휘로 리스킨. 스캔라인은 다크 산출물에만.
- docstring의 `FIG.04` 잔재를 `FIG.05`로 수정 (53c0fd6 재번호 시 누락분).

## 4. 파이프라인 · 파일 구성

| 경로 | 처리 |
|---|---|
| `assets/hero-*.svg`, `research-map-*.svg`, `project-nerv-*.svg`, `field-results-*.svg`, `btn-*.svg` | 내용 교체 (파일명 유지 → README 수정 불필요) |
| `scripts/generate_activity.py` | `PALETTES` 교체 + 템플릿 리스킨 + docstring 수정 |
| `.github/workflows/*` | 불변 |
| `README.md` | 불변 |

- output 브랜치 배포 방식 불변. 산출물 파일명(`build-activity-dark.svg` / `build-activity.svg`) 불변.

## 5. 에러 처리

- 선행 스펙과 동일: Action 실패 시 output 미갱신 → 마지막 정상본 유지. 기여 0건이어도 빈 차트 정상 렌더.
- Chakra Petch 패스 변환 실패/품질 미달 시 시스템 모노 폴백 (§2 타이포).

## 6. 검증

1. **시안 게이트 2단계**: ① FIG.01 다크/라이트 쌍 먼저 제작 → 사용자 승인 → ② 나머지 확산 제작 → 전체 승인 후 push.
2. SVG는 시스템 폰트 + 임베드 패스만 사용 → 로컬 브라우저에서 다크/라이트 각각 확인 (헤드리스 크롬 스크린샷 검증 병행).
3. `generate_activity.py`는 로컬에서 `GITHUB_TOKEN=$(gh auth token)`으로 실행해 산출물 확인, push 후 workflow_dispatch로 재검증.
4. push 후 실제 프로필에서 최종 확인 (camo 캐시로 몇 분 지연 가능).
5. 접근성: 전 SVG `<title>/<desc>` 갱신(NERV 테마 서술로), `prefers-reduced-motion` 대응, 라이트/다크 대비율 확인 (특히 앰버 on 보이드, 레드 on 아이보리).

## 7. 범위 제외

- README 텍스트·섹션 제목 개편 (세계관 전면 개편안은 기각됨)
- R-02 논문 행 추가 (8월 게재 확정 시 별도 작업)
- 좌측 프로필 bio, pinned 구성, whitepaper·대시보드 자체의 변경
