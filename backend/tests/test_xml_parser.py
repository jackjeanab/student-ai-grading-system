from pathlib import Path

from app.services.xml_parser import parse_blockly_xml


def test_parse_blockly_xml_extracts_block_types() -> None:
    xml_content = Path("tests/fixtures/sample_blockly.xml").read_text(encoding="utf-8")

    parsed = parse_blockly_xml(xml_content)

    assert parsed["root_block_types"] == ["board_initializes_setup"]
    assert "delay_custom" in parsed["all_block_types"]
