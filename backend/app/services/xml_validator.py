from xml.etree import ElementTree


def validate_blockly_xml(xml_content: str) -> None:
    try:
        ElementTree.fromstring(xml_content)
    except ElementTree.ParseError as exc:
        raise ValueError("Invalid XML format") from exc
