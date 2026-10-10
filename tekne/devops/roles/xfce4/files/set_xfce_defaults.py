#!/usr/bin/env python3
"""Set XFCE defaults that must exist before the first graphical login."""

import sys
import xml.etree.ElementTree as ET
from pathlib import Path

CHANNELS = {
    "xfce4-session": (
        (("general",), "SaveOnExit", "bool", "false"),
    ),
    "xsettings": (
        (("Net",), "EnableInputFeedbackSounds", "bool", "true"),
        (("Net",), "EnableEventSounds", "bool", "true"),
        (("Net",), "SoundThemeName", "string", "Smooth"),
    ),
    "displays": (
        ((), "Notify", "int", "3"),
        ((), "AutoEnableProfiles", "int", "3"),
    ),
}


def property_node(parent: ET.Element, name: str) -> ET.Element:
    node = next(
        (
            child
            for child in parent
            if child.tag == "property" and child.get("name") == name
        ),
        None,
    )
    if node is None:
        node = ET.SubElement(parent, "property", {"name": name, "type": "empty"})
    return node


def update_channel(config_dir: Path, channel: str) -> bool:
    path = config_dir / f"{channel}.xml"
    if path.exists() and path.stat().st_size > 0:
        tree = ET.parse(path)
        root = tree.getroot()
    else:
        root = ET.Element("channel", {"name": channel, "version": "1.0"})
        tree = ET.ElementTree(root)

    changed = False
    for parents, name, value_type, value in CHANNELS[channel]:
        parent = root
        for parent_name in parents:
            parent = property_node(parent, parent_name)

        node = property_node(parent, name)
        if node.get("type") != value_type or node.get("value") != value:
            node.set("type", value_type)
            node.set("value", value)
            changed = True

    if changed:
        ET.indent(tree, space="  ")
        tree.write(path, encoding="UTF-8", xml_declaration=True)
    return changed


def main() -> int:
    config_dir = Path(sys.argv[1])
    config_dir.mkdir(parents=True, exist_ok=True)
    changed = False
    for channel in CHANNELS:
        changed = update_channel(config_dir, channel) or changed
    if changed:
        print("changed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
