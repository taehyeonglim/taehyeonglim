# 프로젝트 진행 게이지 (Project Progress Gauge) — 설계

- 날짜: 2026-10-10
- 상태: 사용자 승인 대기 (대화 설계 승인 완료)
- 관련: [Open source 섹션 설계](2026-08-17-open-source-section-design.md)

## 1. 목적

README의 Open source 목록(공개 18개)과 접힌 Private 목록(비공개 21개)의 각 항목이 **어느 단계까지 왔는지** 한눈에 보이도록, 항목 바로 아래에 NERV 테마 진행 게이지를 붙인다. 주 사용자는 프로필 주인 본인(기억 보조)이고, 방문자에게도 보인다.

성공 기준:

- 39개 항목 모두 게이지가 붙어 있고, 단계·상태가 데이터 파일과 일치한다.
- 단계 변경은 `data/progress.json` 한 줄 수정 + push로 끝난다 (GitHub 웹 편집 포함).
- 목록과 데이터가 어긋나면 테스트가 실패한다.

## 2. 진행도 모델

완성도 %가 아니라 **단계(phase) + 상태(status)** 로 표현한다. 값은 Claude가 근거로 초안을 채우고 사용자가 확정한다.

| phase | 코드 | 의미 |
|---|---|---|
| 1 | `DESIGN` | 스펙·계획·기술 검증 단계 |
| 2 | `BUILD` | 핵심 기능 개발 중, 공개 배포 없음 |
| 3 | `DEPLOYED` | 라이브 URL 또는 설치 가능한 패키지 존재 |
| 4 | `OPERATIONAL` | 배포 후 지속 개선·확장 중 |
| 5 | `COMPLETE` | 목표 달성, 유지보수만 |

| status | 의미 |
|---|---|
| `active` | 진행 중 |
| `standby` | 보류 (단계는 멈춘 지점을 유지) |

## 3. 데이터 — `data/progress.json`

```json
{
  "NERV": { "phase": 4, "status": "active" },
  "learning-agent": { "phase": 1, "status": "standby" }
}
```

- 키 = GitHub 저장소 이름 그대로 (README 링크·URL과 기계적으로 대조 가능해야 함). 예: `korean-elementary-learning-map-mcp`, `2026-esports-landscape`.
- 키는 `^[A-Za-z0-9._-]+$`만 허용 (파일명·URL로 그대로 쓰임).
- 그 밖의 필드는 두지 않는다 (YAGNI). 근거 메모는 초안 검토 표에서만 쓰고 데이터에 남기지 않는다.

## 4. 게이지 SVG — 시안 C "MAGI 터미널 리드아웃"

- 크기 460×34, viewBox 동일. 레포당 1장, 파일명 `progress/<repo>.svg`.
- 다크/라이트 공용 단일 룩 (기존 NERV 자산과 동일 원칙 — 어두운 캡슐이 라이트 배경에서도 판독됨).
- 구성:
  - 프레임: 배경 `#0a0c12`, 테두리 `#ff6a00` opacity .35.
  - 상단 판독값 (font-size 9, monospace): 좌측 `SYS.PHASE`(`#9a7048`) + `0{p}/05 :: {CODE}`(굵게, active `#ffb000` / standby `#5b6070`).
  - 우측 상태 태그: active `■ ACTIVE`(`#3dff9a`), standby `▲ STANDBY`(`#ffb000`).
  - 하단 바: 트랙 x=10~450, y=19, 높이 8, 트랙색 `#141826`. 채움 폭 = 440 × phase/5.
  - 채움색: active → `#ff6a00`, phase 5 active → `#3dff9a`, standby → 45° 해저드 줄무늬 패턴(`#ffb000` opacity .55, 폭 4/주기 8).
  - 5분할 구분선: x = 10 + 88·i (i=1..4), 배경색 2px 선.
- 패턴 id는 레포별 고유 접미사를 붙인다 (README에 여러 장이 인라인될 일은 없지만 SVG 단독 유효성 유지).
- `<title>`에 `"{repo} — SYS.PHASE 0{p}/05 {CODE} · {STATUS}"`.

## 5. README 배치

각 목록 항목 줄 끝에 `<br>`, 다음 줄에 2칸 들여쓰기로 이미지:

```markdown
- **[edtech-oracle](https://github.com/taehyeonglim/edtech-oracle)** — … `Claude Code`<br>
  <img src="https://raw.githubusercontent.com/taehyeonglim/taehyeonglim/output/progress/edtech-oracle.svg" width="460" alt="edtech-oracle progress">
```

- Private 항목은 링크 없는 `**name** (private)` 형식 그대로, 같은 방식으로 이미지를 붙인다.
- alt는 `"<repo> progress"`로 고정한다. 단계를 alt에 넣으면 데이터 변경 때마다 README도 고쳐야 해서 "JSON 한 줄 수정으로 끝" 기준이 깨진다. 단계 판독값은 SVG `<title>`이 담당한다.
- Open source 헤더 패널 SVG(18 카드)는 변경하지 않는다.

## 6. 생성 파이프라인

### 스크립트 `scripts/generate_progress.py`

- 표준 라이브러리만 사용 (기존 `generate_activity.py`와 동일 원칙).
- 구조:
  - `PHASES` 상수, `validate(data) -> None` (오류 시 `ValueError`), `render_gauge(repo, phase, status) -> str` (순수 함수), `main(argv)`.
- CLI: `python3 scripts/generate_progress.py --data data/progress.json --out dist/progress`.
- 검증 실패(phase 범위 밖, status 오타, 키 형식 위반, JSON 파싱 오류)는 비정상 종료 — 깨진 게이지를 조용히 배포하지 않는다.

### CI — `.github/workflows/blueprint-activity.yml`

- `build` job의 "Generate activity SVGs" 다음에 단계 추가:
  `python3 scripts/generate_progress.py --data data/progress.json --out dist/progress`
- 같은 `dist/`가 `output` 브랜치로 배포되므로 배포 단계는 그대로. 트리거(push to main, 12시간 cron, 수동)도 그대로.

## 7. 테스트 — `tests/test_generate_progress.py` (TDD)

1. 렌더
   - phase 1~5 각각 채움 폭이 88·phase.
   - phase 5 active는 초록 채움, standby는 해저드 패턴 참조, active는 `■ ACTIVE`, standby는 `▲ STANDBY`.
   - 출력이 `xml.dom.minidom`으로 파싱됨.
2. 검증
   - phase 0·6·문자열, status `"paused"`, 키 `"../x"`에서 `ValueError`.
3. CLI
   - 임시 디렉터리에 데이터 → `<repo>.svg` 파일 수 = 항목 수.
4. README 동기화 (실제 `README.md` + `data/progress.json` 대상)
   - Open source 항목(링크된 `github.com/taehyeonglim/<repo>`)과 Private 항목(`**<repo>** (private)`)의 레포 집합 == 데이터 키 집합.
   - 각 항목 바로 다음 줄 이미지 src가 `output/progress/<그 레포>.svg`.
   - 각 이미지 alt == `"<repo> progress"`.

## 8. 초기 단계값 채우기

Claude가 레포별 근거로 초안을 만들고 표(레포 · 제안 phase/status · 근거 한 줄)로 제시, 사용자가 수정 사항만 지정한다. 근거 규칙:

- 라이브 URL·homepage·패키지 → DEPLOYED 이상.
- 최근 30일 커밋 활동 + 배포 → OPERATIONAL.
- README에 Phase 0·설계 단계 명시 → DESIGN.
- 배포 후 장기간 커밋 없음 → COMPLETE 또는 STANDBY 후보 (판단 애매하면 사용자에게 표에서 질문).

## 9. 부수 정리

- `.gitignore`에 `.superpowers/` 추가 (브레인스토밍 산출물 커밋 방지).

## 10. 범위 밖

- 완성도 % 표기, 자동 단계 산출, 헤더 패널 카드 내 게이지, 단계 이력·날짜 기록.
