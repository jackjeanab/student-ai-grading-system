import subprocess
import sys
import unittest
from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "pdf_to_markdown.py"
SOURCE_DIR = ROOT / "texts"


class PdfToMarkdownTest(unittest.TestCase):
    def test_single_pdf_generates_markdown_with_image_notes(self) -> None:
        pdf_path = next(SOURCE_DIR.glob("Chapter01*.pdf"))
        temp_root = ROOT / ".tmp-tests"
        temp_root.mkdir(exist_ok=True)
        output_dir = temp_root / "single_pdf_case"
        shutil.rmtree(output_dir, ignore_errors=True)
        output_dir.mkdir(parents=True, exist_ok=True)

        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--input",
                str(pdf_path),
                "--output-dir",
                str(output_dir),
            ],
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertEqual(result.returncode, 0, msg=result.stderr or result.stdout)

        markdown_path = output_dir / f"{pdf_path.stem}.md"
        self.assertTrue(markdown_path.exists(), msg="markdown file was not created")

        markdown_text = markdown_path.read_text(encoding="utf-8")
        self.assertIn("## 第 1 頁", markdown_text)
        self.assertIn("圖片說明", markdown_text)


if __name__ == "__main__":
    unittest.main()
