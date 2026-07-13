# GitHub 프로필 블루프린트 리디자인 — 디자인 스펙

- 날짜: 2026-07-13
- 대상 저장소: `taehyeonglim/taehyeonglim` (GitHub 프로필 README)
- 범위: 히어로 배너 / 아키텍처 다이어그램 / NERV 화이트페이퍼 카드 / 빌드 액티비티 차트 (4개 에셋)

## 1. 목표

기존 다크 네이비 + 네온 그라데이션 컨셉을 버리고, 4개 에셋 전체를 **엔지니어링 블루프린트(제도 도면)** 비주얼 아이덴티티로 재설계한다. "시스템 설계자"라는 정체성을 도면 언어로 표현하되, 각 에셋의 콘텐츠(문구·정보 구성)는 유지한다.

**확정된 결정**

| 결정 항목 | 선택 |
|---|---|
| 컨셉 | 블루프린트 도면 (완전 신규) |
| 라이트/다크 | 다크 = 클래식 청사진, 라이트 = 화이트프린트 |
| 액티비티 차트 | 외부 서비스 제거, GitHub Action 자체 생성으로 교체 (스네이크 제거) |
| 콘텐츠 | 기존 문구·구성요소 유지, 스킨만 교체 |
| 모션 | B안 — 은은한 제도 모션 (dash-flow, 스캔라인, 마커 blink) |

## 2. 공통 디자인 시스템 "BLUEPRINT"

### 색상

| 역할 | 다크 (청사진) | 라이트 (화이트프린트) |
|---|---|---|
| 바탕 | 프러시안 블루 `#0d2a55 → #123a75` 미세 그라데이션 | 종이 화이트 `#fafcff` + 미색 음영 |
| 제도선/잉크 | 백청 `#dbeafe`~`#eff6ff` | 청색 잉크 `#1e40af` |
| 모눈 | 흰 선 4~5% 투명도 | 청색 선 6~7% 투명도 |
| 포인트 | 레드라인 `#f87171` | 레드라인 `#dc2626` |

- 모눈은 8px 세밀 + 40px 굵은 선의 2중 격자.
- 레드라인은 도면 검수 문화(redline markup)의 메타포 — 강조 라벨·스탬프·핵심 수치에만 제한 사용.

### 타이포그래피

- 전 에셋 모노스페이스: `ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, "Liberation Mono", monospace`
- 제목은 대문자 + 넓은 자간 (도면 레터링). GitHub `<img>` 렌더링은 외부 폰트를 로드할 수 없으므로 시스템 스택만 사용한다.

### 도면 어휘 (전 에셋 공통 장치)

- **도곽(border frame)**: 이중 테두리 + 가장자리 눈금 틱 + 모서리 등록 마크(+)
- **타이틀 블록**: 우하단 구획표 — `FIG.NN / DWG NO. TL-2026-NN / REV 2026.07 / SCALE 1:1`
- **치수선·인출선**: 화살표 dimension line, `ø45 AGENTS` 식 기술 표기
- **FIG 연번**: FIG.01(히어로) → FIG.02(아키텍처) → FIG.03(NERV) → FIG.04(액티비티) — 4개 에셋이 한 도면집(drawing set)으로 읽히게 한다.

### 모션 (B안 — 은은한 제도 모션)

- 연결선 dash-flow (9~18s 느린 주기)
- 도면 위를 지나는 가는 스캔라인 1개
- 포인트 마커 blink
- 전부 SVG 내부 CSS `@keyframes`. `prefers-reduced-motion: reduce`에서 전체 정지.

## 3. 에셋별 설계

### FIG.01 — 히어로 배너 (1200×320, `assets/hero-dark.svg` / `hero-light.svg` 교체)

- 좌측 타이포 블록: 기존 문구 유지 — eyebrow `TAEHYEONG LIM, PH.D.`, 메인 `HUMAN × AI` / `CO-INTELLIGENCE SYSTEMS`, 서브 "Building multi-agent systems that think, verify, and work with humans." `×` 기호만 레드라인 컬러.
- 캡슐 3개(`AI CO-SCIENTIST` / `MULTI-AGENT SYSTEMS` / `HUMAN-IN-THE-LOOP`) → 각진 도면 스탬프 라벨.
- 우측: Human×AI 래티스를 도면 문법으로 재해석 — 센터라인 크로스헤어 원 2개(HUMAN INTENT / AI AGENCY 인출선 라벨), 중앙 `×`, 치수선.
- 우하단 타이틀 블록. 모션: 래티스 연결선 dash-flow + 세로 스캔라인.

### FIG.02 — 아키텍처 다이어그램 (1200×440, `assets/research-map-dark.svg` / `-light.svg` 교체)

- 허브-스포크 구성 유지, 곡선/사선 연결을 **직교 배선(90° 꺾임, 회로도식)**으로 교체.
- 중앙 `NERV / MAGI · AI Co-Scientist` = 메인 어셈블리 박스(이중 테두리). 서브텍스트 "orchestrate · verify · remember · act" 유지.
- 6개 역량 노드 = 부품 박스 + 파트 넘버: `PT-01 Multi-Agent Orchestration` ~ `PT-06 Research Automation`. 기존 문구·서브텍스트 유지.
- **Human in the Loop 박스만 레드라인 강조** (인간 = 검수자 의미).
- 명령 흐름 = 실선, 검증 피드백 = 점선. 미니 범례 추가.
- 모션: 배선 dash-flow, HITL 마커 blink.

### FIG.03 — NERV 카드 (1200×270, `assets/project-nerv-dark.svg` / `-light.svg` 신규 2본)

- **라이트 대응 신설**: 기존 다크 단일본(`project-nerv.svg`) 삭제, 2본 + `<picture>` 태그로 교체.
- 콘텐츠 유지: `NERV SYSTEM WHITEPAPER` 타이틀, 45-agent 설명문, 캡슐 3개(45 AI AGENTS / 7 SYSTEM ROLES / MAGI VALIDATION), 방사형 7노드, `READ THE WHITEPAPER →`.
- 이 카드만 레드라인 비중 상향(검증 시스템 정체성): 좌측 세로 레드 등록선, 우상단 **"MAGI VALIDATED" 승인 스탬프**(살짝 기울임).
- 방사형 7노드 → 중앙 `RESEARCH CORE` + 방사 인출선 + `ø 7 ROLES` 치수 표기.
- 카드 전체가 화이트페이퍼 링크(기존과 동일).

### FIG.04 — 빌드 액티비티 차트 (1200×340, 자체 생성)

- GitHub Action이 GraphQL `contributionsCollection.contributionCalendar`로 최근 1년 데이터 조회 → **주간 합계 52개 막대 차트**를 도면 스타일로 렌더.
- 2중 모눈 위 막대, 월 라벨 눈금, 상단 주석 `Σ N CONTRIBUTIONS / 365 DAYS`.
- 최고 주간에 레드라인 인출선 콜아웃 `PEAK — n/wk` (자동 계산).
- 다크/라이트 2본을 output 브랜치에 커밋. 기존 Vercel 라인차트·스네이크 애니메이션은 제거.
- 모션: 스캔라인 1개 (템플릿에 포함).

## 4. 파이프라인 · 파일 구성

| 경로 | 처리 |
|---|---|
| `assets/hero-dark.svg` / `hero-light.svg` | 교체 (파일명 유지 → README 수정 불필요) |
| `assets/research-map-dark.svg` / `-light.svg` | 교체 (파일명 유지) |
| `assets/project-nerv-dark.svg` / `-light.svg` | 신규 2본, 기존 `project-nerv.svg` 삭제 |
| `scripts/generate_activity.py` | 신규 — Python 표준 라이브러리만 사용 (의존성 0). GraphQL 조회 + SVG 2본 렌더 |
| `.github/workflows/blueprint-activity.yml` | `snake.yml` 삭제 후 대체. 트리거 동일: cron 12h + main push + workflow_dispatch |

- output 브랜치 배포는 기존 방식(`crazy-max/ghaction-github-pages@v4`) 재사용. 산출물: `build-activity-dark.svg` / `build-activity.svg`.
- 인증: Actions 기본 `GITHUB_TOKEN`으로 충분 (public 기여 데이터).

## 5. README.md 변경

- FIG.03: `project-nerv.svg` 단일 `<img>` → dark/light `<picture>` 태그.
- FIG.04: activity-graph·스네이크 마크업 제거 → output 브랜치 raw URL의 `<picture>` 태그.
- FIG.01/02는 파일명 유지로 변경 불필요. 나머지 텍스트 유지.
- shields.io 뱃지 3개는 범위 밖 — 이번에는 유지 (후속 작업 후보: 도면 스타일 자체 버튼).

## 6. 에러 처리

- Action의 GraphQL 조회 실패 시 job 실패로 종료 → output 브랜치를 덮어쓰지 않으므로 README는 마지막 정상본을 계속 표시.
- 기여 데이터가 비어 있어도(0건) 빈 도면으로 정상 렌더.

## 7. 검증

1. SVG는 시스템 폰트만 사용 → 로컬 브라우저에서 직접 열어 다크/라이트 각각 확인. **push 전에 사용자 시안 승인 필수.**
2. `generate_activity.py`는 로컬에서 `GITHUB_TOKEN=$(gh auth token)`으로 실행해 산출물 확인.
3. push 후 실제 프로필 페이지에서 최종 확인 (camo 캐시로 갱신 지연 몇 분 가능).
4. Action은 workflow_dispatch 수동 실행으로 output 산출물 검증.
5. 접근성: 모든 SVG에 `<title>/<desc>` 유지, `prefers-reduced-motion` 대응.

## 8. 범위 제외

- shields.io 뱃지 교체, README 텍스트 개편, 좌측 프로필(bio 등), pinned 구성 — 모두 이번 작업 범위 밖.
