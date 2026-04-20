from __future__ import annotations

import argparse
import hashlib
import re
from dataclasses import dataclass
from pathlib import Path

from pypdf import PdfReader


CAPTION_RE = re.compile(r"^圖\s*\d+\s*-\s*\d+.*")
SECTION_RE = re.compile(r"^\d+\s*-\s*\d+\s+.+")


@dataclass
class SavedImage:
    index: int
    relative_path: str
    caption: str
    description: str


def normalize_line(line: str) -> str:
    return re.sub(r"\s+", " ", line).strip()


def extract_lines_from_text(text: str) -> list[str]:
    return [normalize_line(line) for line in text.splitlines() if normalize_line(line)]


def find_section_title(lines: list[str]) -> str:
    for line in lines:
        if SECTION_RE.match(line):
            return line
    return lines[0] if lines else "本頁內容"


def find_captions(lines: list[str]) -> list[str]:
    return [line for line in lines if CAPTION_RE.match(line)]


def pick_context(lines: list[str], captions: list[str]) -> str:
    ignored = set(captions)
    body_lines = [
        line
        for line in lines
        if line not in ignored and not CAPTION_RE.match(line) and len(line) > 8
    ]
    if not body_lines:
        return "本頁重點內容"
    snippet = " ".join(body_lines[:2])
    return snippet[:90].rstrip("，。； ")


def build_description(
    section_title: str,
    context: str,
    caption: str,
    image_index: int,
    image_total: int,
) -> str:
    caption_body = re.sub(r"^圖\s*\d+\s*-\s*\d+\s*", "", caption).strip()
    if caption_body:
        return (
            f"此圖對應「{caption_body}」，位於「{section_title}」相關內容中，"
            f"主要用來輔助說明 {context}。"
        )
    if image_total == 1:
        return f"此圖位於「{section_title}」頁面，主要用來輔助說明 {context}。"
    return (
        f"這是本頁第 {image_index} 張重點圖片，位於「{section_title}」相關內容中，"
        f"主要用來輔助說明 {context}。"
    )


def keep_image(area: int, largest_area: int, image_count: int, order_index: int) -> bool:
    if image_count <= 3:
        return area >= 8_000
    threshold = max(25_000, int(largest_area * 0.12))
    return area >= threshold and order_index < 4


def save_page_images(
    page,
    output_dir: Path,
    base_name: str,
    page_number: int,
    captions: list[str],
    section_title: str,
    context: str,
) -> list[SavedImage]:
    images = list(page.images)
    if not images:
        return []

    areas = [img.image.size[0] * img.image.size[1] for img in images]
    largest_area = max(areas)
    seen_hashes: set[str] = set()
    saved: list[SavedImage] = []
    image_dir = output_dir / f"{base_name}_images"
    image_dir.mkdir(parents=True, exist_ok=True)

    kept_order = 0
    for raw_index, img in enumerate(images, start=1):
        width, height = img.image.size
        area = width * height
        if not keep_image(area, largest_area, len(images), kept_order):
            continue

        image_bytes = img.data
        digest = hashlib.sha1(image_bytes).hexdigest()
        if digest in seen_hashes:
            continue
        seen_hashes.add(digest)

        kept_order += 1
        suffix = Path(img.name).suffix or ".png"
        filename = f"page_{page_number:03d}_img_{kept_order:02d}{suffix.lower()}"
        image_path = image_dir / filename
        img.image.save(image_path)

        caption = captions[kept_order - 1] if kept_order - 1 < len(captions) else ""
        description = build_description(
            section_title=section_title,
            context=context,
            caption=caption,
            image_index=kept_order,
            image_total=len(images),
        )
        saved.append(
            SavedImage(
                index=kept_order,
                relative_path=f"{base_name}_images/{filename}",
                caption=caption,
                description=description,
            )
        )

    return saved


def render_page_markdown(page_number: int, lines: list[str], images: list[SavedImage]) -> str:
    parts = [f"## 第 {page_number} 頁", ""]
    if lines:
        parts.extend(lines)
    else:
        parts.append("（本頁未擷取到可辨識文字）")

    if images:
        parts.extend(["", "### 圖片", ""])
        for image in images:
            alt_text = image.caption or f"第 {page_number} 頁圖片 {image.index}"
            parts.append(f"![{alt_text}]({image.relative_path})")
            parts.append("")
            parts.append(f"圖片說明：{image.description}")
            parts.append("")

    return "\n".join(parts).rstrip()


def convert_pdf(pdf_path: Path, output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    markdown_path = output_dir / f"{pdf_path.stem}.md"

    reader = PdfReader(str(pdf_path))
    markdown_sections = [f"# {pdf_path.stem}", ""]
    for page_number, reader_page in enumerate(reader.pages, start=1):
        text = reader_page.extract_text() or ""
        lines = extract_lines_from_text(text)
        captions = find_captions(lines)
        section_title = find_section_title(lines)
        context = pick_context(lines, captions)
        images = save_page_images(
            page=reader_page,
            output_dir=output_dir,
            base_name=pdf_path.stem,
            page_number=page_number,
            captions=captions,
            section_title=section_title,
            context=context,
        )
        markdown_sections.append(render_page_markdown(page_number, lines, images))
        markdown_sections.append("")

    markdown_path.write_text("\n".join(markdown_sections).rstrip() + "\n", encoding="utf-8")
    return markdown_path


def iter_pdfs(input_path: Path) -> list[Path]:
    if input_path.is_file():
        return [input_path]
    return sorted(input_path.glob("*.pdf"))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Convert PDF files into Markdown.")
    parser.add_argument("--input", required=True, help="PDF file or directory containing PDFs.")
    parser.add_argument(
        "--output-dir",
        required=True,
        help="Directory where Markdown files and extracted images will be written.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    input_path = Path(args.input)
    output_dir = Path(args.output_dir)

    pdf_paths = iter_pdfs(input_path)
    if not pdf_paths:
        raise SystemExit(f"No PDF files found under: {input_path}")

    for pdf_path in pdf_paths:
        markdown_path = convert_pdf(pdf_path, output_dir)
        print(f"Converted: {pdf_path.name} -> {markdown_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
