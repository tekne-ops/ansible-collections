#!/usr/bin/env python3
"""Set xfwm4 compositor vertical sync in an xfconf channel file."""

import sys
import xml.etree.ElementTree as ET
from pathlib import Path

WANTED = (
    ("use_compositing", "bool", "true"),
    ("vblank_mode", "string", "glx"),
    ("unredirect_overlays", "bool", "false"),
)


def main() -> int:
    path = Path(sys.argv[1])
    path.parent.mkdir(parents=True, exist_ok=True)

    if path.exists() and path.stat().st_size > 0:
        tree = ET.parse(path)
        root = tree.getroot()
    else:
        root = ET.Element("channel", {"name": "xfwm4", "version": "1.0"})
        tree = ET.ElementTree(root)

    general = next(
        (
            child
            for child in list(root)
            if child.tag == "property" and child.get("name") == "general"
        ),
        None,
    )
    if general is None:
        general = ET.SubElement(root, "property", {"name": "general", "type": "empty"})

    changed = False
    for name, value_type, value in WANTED:
        node = next(
            (
                child
                for child in list(general)
                if child.tag == "property" and child.get("name") == name
            ),
            None,
        )
        if node is None:
            ET.SubElement(
                general,
                "property",
                {"name": name, "type": value_type, "value": value},
            )
            changed = True
        elif node.get("type") != value_type or node.get("value") != value:
            node.set("type", value_type)
            node.set("value", value)
            changed = True

    if changed:
        ET.indent(tree, space="  ")
        tree.write(path, encoding="UTF-8", xml_declaration=True)
        print("changed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
