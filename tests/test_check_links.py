import io
import os
import sys
import tempfile
import unittest
import urllib.error

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
import check_links as cl


class FakeResponse:
    def __init__(self, status):
        self.status = status

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


class FakeOpener:
    """지정한 시나리오를 순서대로 돌려주는 opener. 호출 이력을 기록한다."""

    def __init__(self, *outcomes):
        self.outcomes = list(outcomes)
        self.calls = []  # (method, url)

    def __call__(self, req, timeout=None):
        self.calls.append((req.get_method(), req.full_url))
        outcome = self.outcomes.pop(0) if self.outcomes else 200
        if isinstance(outcome, Exception):
            raise outcome
        if outcome >= 400:
            raise urllib.error.HTTPError(req.full_url, outcome, "err", {}, None)
        return FakeResponse(outcome)


def http_error(code):
    return urllib.error.HTTPError("http://x", code, "err", {}, None)


class ExtractUrlsTest(unittest.TestCase):
    def test_pulls_html_attributes(self):
        md = ('<a href="https://a.example/"><img alt="x" src="https://b.example/i.svg">'
              '<source srcset="https://c.example/d.svg"></a>')
        self.assertEqual(cl.extract_urls(md),
                         ["https://a.example/", "https://b.example/i.svg",
                          "https://c.example/d.svg"])

    def test_pulls_markdown_links(self):
        # HTML 속성만 긁으면 놓치는 형태 — README의 CV·DOI 링크가 여기 해당한다
        md = "연구실적: [taehyeonglim.github.io/cv](https://taehyeonglim.github.io/cv/)"
        self.assertIn("https://taehyeonglim.github.io/cv/", cl.extract_urls(md))

    def test_dedupes_and_sorts(self):
        md = ('<a href="https://b.example/">x</a> [y](https://a.example/) '
              '<img src="https://b.example/">')
        self.assertEqual(cl.extract_urls(md), ["https://a.example/", "https://b.example/"])

    def test_skips_relative_and_non_http(self):
        md = ('<a href="#anchor">a</a> <a href="mailto:x@y.z">b</a> '
              '<img src="assets/local.svg"> [c](https://ok.example/)')
        self.assertEqual(cl.extract_urls(md), ["https://ok.example/"])

    def test_reads_real_readme(self):
        readme = os.path.join(os.path.dirname(__file__), "..", "README.md")
        with open(readme, encoding="utf-8") as f:
            urls = cl.extract_urls(f.read())
        self.assertTrue(all(u.startswith("https://") for u in urls))
        # 마크다운 링크로만 존재하는 CV 링크가 반드시 잡혀야 한다
        self.assertIn("https://taehyeonglim.github.io/cv/", urls)


class CheckUrlTest(unittest.TestCase):
    def test_success_on_first_attempt(self):
        op = FakeOpener(200)
        ok, detail = cl.check_url("https://x.example/", op, sleep=lambda s: None)
        self.assertTrue(ok)
        self.assertEqual(detail, "200")
        self.assertEqual(len(op.calls), 1)

    def test_retries_transient_error_then_succeeds(self):
        op = FakeOpener(urllib.error.URLError("timed out"), 200)
        ok, detail = cl.check_url("https://x.example/", op, sleep=lambda s: None)
        self.assertTrue(ok)
        self.assertEqual(len(op.calls), 2)

    def test_retries_server_error(self):
        op = FakeOpener(http_error(503), http_error(503), 200)
        ok, _ = cl.check_url("https://x.example/", op, sleep=lambda s: None)
        self.assertTrue(ok)
        self.assertEqual(len(op.calls), 3)

    def test_gives_up_after_attempts(self):
        op = FakeOpener(http_error(503), http_error(503), http_error(503))
        ok, detail = cl.check_url("https://x.example/", op, attempts=3, sleep=lambda s: None)
        self.assertFalse(ok)
        self.assertIn("503", detail)
        self.assertEqual(len(op.calls), 3)

    def test_404_fails_without_retry(self):
        # 404는 일시적 오류가 아니므로 재시도로 시간을 낭비하지 않는다
        op = FakeOpener(http_error(404))
        ok, detail = cl.check_url("https://x.example/", op, sleep=lambda s: None)
        self.assertFalse(ok)
        self.assertEqual(detail, "404")
        self.assertEqual(len(op.calls), 1)

    def test_head_rejected_falls_back_to_get(self):
        # 일부 서버는 HEAD를 거부한다 (405/501/403)
        op = FakeOpener(http_error(405), 200)
        ok, _ = cl.check_url("https://x.example/", op, sleep=lambda s: None)
        self.assertTrue(ok)
        self.assertEqual([m for m, _ in op.calls], ["HEAD", "GET"])

    def test_sends_browser_user_agent(self):
        # DOI 리졸버는 봇 UA에 403을 준다 — 브라우저 UA가 없으면 상시 오탐
        op = FakeOpener(200)
        cl.check_url("https://x.example/", op, sleep=lambda s: None)
        self.assertIn("Mozilla", cl.USER_AGENT)


class SummaryTest(unittest.TestCase):
    def test_marks_failures(self):
        rows = [("https://ok.example/", True, "200"),
                ("https://bad.example/", False, "404")]
        out = cl.format_summary(rows)
        self.assertIn("https://bad.example/", out)
        self.assertIn("404", out)
        self.assertIn("1", out)  # 실패 건수


class MainTest(unittest.TestCase):
    def _readme(self, td, body):
        path = os.path.join(td, "README.md")
        with open(path, "w", encoding="utf-8") as f:
            f.write(body)
        return path

    def test_exit_zero_when_all_ok(self):
        with tempfile.TemporaryDirectory() as td:
            path = self._readme(td, '<a href="https://a.example/">x</a>')
            code = cl.main(["--readme", path], opener=FakeOpener(200),
                           sleep=lambda s: None, stream=io.StringIO())
            self.assertEqual(code, 0)

    def test_exit_one_when_any_fails(self):
        with tempfile.TemporaryDirectory() as td:
            path = self._readme(td, '<a href="https://a.example/">x</a>')
            code = cl.main(["--readme", path], opener=FakeOpener(http_error(404)),
                           sleep=lambda s: None, stream=io.StringIO())
            self.assertEqual(code, 1)

    def test_writes_step_summary_when_env_set(self):
        with tempfile.TemporaryDirectory() as td:
            path = self._readme(td, '<a href="https://a.example/">x</a>')
            summary = os.path.join(td, "summary.md")
            os.environ["GITHUB_STEP_SUMMARY"] = summary
            try:
                cl.main(["--readme", path], opener=FakeOpener(200),
                        sleep=lambda s: None, stream=io.StringIO())
            finally:
                del os.environ["GITHUB_STEP_SUMMARY"]
            with open(summary, encoding="utf-8") as f:
                self.assertIn("https://a.example/", f.read())


if __name__ == "__main__":
    unittest.main()
