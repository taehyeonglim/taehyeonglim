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
