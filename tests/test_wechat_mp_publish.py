from __future__ import annotations

import importlib.util
import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "wechat-article-publish" / "scripts" / "wechat_mp_publish.py"

spec = importlib.util.spec_from_file_location("wechat_mp_publish", SCRIPT)
assert spec and spec.loader
wechat_mp_publish = importlib.util.module_from_spec(spec)
spec.loader.exec_module(wechat_mp_publish)


class WechatMpPublishTest(unittest.TestCase):
    def test_normalize_wechat_lists_removes_whitespace_between_items(self) -> None:
        content = "<ol>\n<li>AI 读很多文件。</li>\n<li>AI 输出很多修改。</li>\n</ol>"

        normalized = wechat_mp_publish.normalize_wechat_lists(content)

        self.assertEqual(
            normalized,
            "<ol><li>AI 读很多文件。</li><li>AI 输出很多修改。</li></ol>",
        )

    def test_simple_markdown_fallback_preserves_lists(self) -> None:
        content = "\n".join(
            [
                "这类循环最烧 Token：",
                "",
                "1. AI 读很多文件。",
                "2. AI 输出很多修改。",
                "",
                "常见 Agent：",
                "",
                "- 一个做需求拆解",
                "- 一个做 Code Review",
            ]
        )

        rendered = wechat_mp_publish.simple_markdown_to_html(content)

        self.assertIn("<ol><li>AI 读很多文件。</li><li>AI 输出很多修改。</li></ol>", rendered)
        self.assertIn("<ul><li>一个做需求拆解</li><li>一个做 Code Review</li></ul>", rendered)

    def test_draft_dry_run_compacts_markdown_lists(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            article = Path(tmpdir) / "article.md"
            article.write_text(
                "\n".join(
                    [
                        "# Test Article",
                        "",
                        "这类循环最烧 Token：",
                        "",
                        "1. AI 读很多文件。",
                        "2. AI 输出很多修改。",
                        "",
                        "常见 Agent：",
                        "",
                        "- 一个做需求拆解",
                        "- 一个做 Code Review",
                    ]
                ),
                encoding="utf-8",
            )

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "draft",
                    "--article",
                    str(article),
                    "--thumb-media-id",
                    "TEST_THUMB",
                    "--dry-run",
                ],
                check=True,
                capture_output=True,
                text=True,
            )

        content = json.loads(result.stdout)["draft_payload"]["articles"][0]["content"]

        self.assertEqual(0, len(re.findall(r"<li[^>]*>\s*</li>", content, re.I)))
        self.assertIn("<ol><li>AI 读很多文件。</li><li>AI 输出很多修改。</li></ol>", content)
        self.assertIn("<ul><li>一个做需求拆解</li><li>一个做 Code Review</li></ul>", content)


if __name__ == "__main__":
    unittest.main()
