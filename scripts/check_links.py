#!/usr/bin/env python3
"""README의 외부 링크 상태 검사기.

프로필 README는 별도 저장소(nerv-whitepaper 등)의 URL 구조를 하드코딩해
참조하므로, 상대 사이트가 재편되면 조용히 404가 된다. 이 스크립트가
주기적으로 전수 확인하고 깨진 링크가 있으면 0이 아닌 코드로 종료한다.
표준 라이브러리만 사용. opener 주입으로 네트워크 없이 테스트 가능.
"""
import argparse
import os
import re
import sys
import time
import urllib.error
import urllib.request

# DOI 리졸버 등은 봇 UA에 403을 준다. 브라우저 UA가 없으면 상시 오탐이 난다.
USER_AGENT = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
              "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36")

TIMEOUT = 20
ATTEMPTS = 3

# HTML 속성(href/src/srcset)과 마크다운 링크 [텍스트](url) 양쪽을 모두 잡는다.
# 속성만 긁으면 README 하단의 CV·DOI 마크다운 링크를 통째로 놓친다.
ATTR_RE = re.compile(r'(?:href|src|srcset)\s*=\s*"([^"]+)"')
MD_LINK_RE = re.compile(r'\]\(\s*(https?://[^\s)]+)\s*\)')

# 일시적 장애로 보고 재시도할 상태코드. 4xx는 재시도해도 답이 같다.
RETRY_CODES = {408, 425, 429, 500, 502, 503, 504}
# HEAD를 거부하는 서버가 있다. 이 경우 GET으로 다시 시도한다.
HEAD_REJECTED = {400, 403, 405, 501}


def extract_urls(text):
    """README 본문에서 검사 대상 https URL을 중복 없이 정렬해 반환한다."""
    found = set()
    for value in ATTR_RE.findall(text):
        # srcset 은 "url 1x, url 2x" 형태일 수 있다
        for part in value.split(","):
            url = part.strip().split(" ")[0]
            if url.startswith("http://") or url.startswith("https://"):
                found.add(url)
    found.update(MD_LINK_RE.findall(text))
    return sorted(found)


def _request(url, method):
    return urllib.request.Request(url, method=method,
                                  headers={"User-Agent": USER_AGENT})


def check_url(url, opener=None, attempts=ATTEMPTS, sleep=time.sleep):
    """(성공 여부, 상세) 를 반환한다. 상세는 상태코드 또는 오류 문자열."""
    opener = opener or urllib.request.urlopen
    method = "HEAD"
    detail = "?"
    for attempt in range(1, attempts + 1):
        try:
            with opener(_request(url, method), timeout=TIMEOUT) as resp:
                status = getattr(resp, "status", None) or resp.getcode()
            return True, str(status)
        except urllib.error.HTTPError as e:
            detail = str(e.code)
            if method == "HEAD" and e.code in HEAD_REJECTED:
                method = "GET"          # 백오프 없이 즉시 GET으로 재시도
                continue
            if e.code not in RETRY_CODES:
                return False, detail    # 404 등은 확정 — 재시도로 시간 낭비하지 않는다
        except Exception as e:          # URLError, socket.timeout, ssl 오류 등
            detail = "%s: %s" % (type(e).__name__, e)
        if attempt < attempts:
            sleep(attempt)              # 1s, 2s 백오프
    return False, detail


def format_summary(rows):
    """Actions 요약 페이지에 붙일 마크다운 표를 만든다."""
    failed = [r for r in rows if not r[1]]
    lines = ["## README 링크 검사", ""]
    lines.append("전체 %d개 · 정상 %d개 · **실패 %d개**"
                 % (len(rows), len(rows) - len(failed), len(failed)))
    lines += ["", "| 상태 | 결과 | URL |", "|---|---|---|"]
    for url, ok, detail in rows:
        lines.append("| %s | `%s` | %s |" % ("✅" if ok else "❌", detail, url))
    return "\n".join(lines) + "\n"


def main(argv=None, opener=None, sleep=time.sleep, stream=None):
    parser = argparse.ArgumentParser(description="README 외부 링크 상태 검사")
    parser.add_argument("--readme", default="README.md")
    parser.add_argument("--attempts", type=int, default=ATTEMPTS)
    args = parser.parse_args(argv)
    out = stream or sys.stdout

    with open(args.readme, encoding="utf-8") as f:
        urls = extract_urls(f.read())

    rows = []
    for url in urls:
        ok, detail = check_url(url, opener, attempts=args.attempts, sleep=sleep)
        rows.append((url, ok, detail))
        print("%s %-6s %s" % ("OK  " if ok else "FAIL", detail, url), file=out)

    summary = format_summary(rows)
    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary_path:
        with open(summary_path, "a", encoding="utf-8") as f:
            f.write(summary)

    failed = [r for r in rows if not r[1]]
    print("\n%d/%d 정상, %d 실패" % (len(rows) - len(failed), len(rows), len(failed)),
          file=out)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
