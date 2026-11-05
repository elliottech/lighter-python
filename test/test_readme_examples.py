"""Keep the hand-maintained README example links usable after moves."""
from pathlib import Path
import re
import unittest
from urllib.parse import unquote, urlsplit


class TestReadmeExamples(unittest.TestCase):
    def test_example_links_resolve_in_checkout(self):
        root = Path(__file__).resolve().parents[1]
        readme = (root / "README.md").read_text(encoding="utf-8")
        section = readme.split("## Examples", 1)[1].split(
            "<!-- AUTOGEN:API_ENDPOINTS -->", 1
        )[0]
        targets = re.findall(r"\[[^\]]*\]\(([^)]+)\)", section)
        self.assertTrue(targets, "README example links must not disappear")
        for target in targets:
            parsed = urlsplit(target)
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            with self.subTest(target=target):
                self.assertTrue(
                    (root / unquote(parsed.path)).exists(),
                    "README example target is missing: " + target,
                )


if __name__ == "__main__":
    unittest.main()
