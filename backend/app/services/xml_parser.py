from xml.etree import ElementTree


BLOCKLY_NS = "https://developers.google.com/blockly/xml"


def parse_blockly_xml(xml_content: str) -> dict[str, list[str]]:
    root = ElementTree.fromstring(xml_content)
    blocks = root.findall(f".//{{{BLOCKLY_NS}}}block")
    root_blocks = root.findall(f"{{{BLOCKLY_NS}}}block")

    return {
        "root_block_types": [
            block.attrib["type"] for block in root_blocks if "type" in block.attrib
        ],
        "all_block_types": [
            block.attrib["type"] for block in blocks if "type" in block.attrib
        ],
    }
