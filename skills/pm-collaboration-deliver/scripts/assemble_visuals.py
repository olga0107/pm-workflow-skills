#!/usr/bin/env python3
"""Replace visual placeholders in Markdown with validated image references."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path


def assemble(draft: Path, mapping_path: Path, output: Path) -> tuple[list[str], str]:
    text = draft.read_text(encoding="utf-8")
    mapping = json.loads(mapping_path.read_text(encoding="utf-8"))
    items = mapping.get("visuals") if isinstance(mapping, dict) else None
    if not isinstance(items, list):
        return ["mapping.visuals must be an array"], text
    errors: list[str] = []
    seen: set[str] = set()
    for index, item in enumerate(items):
        visual_id = item.get("id")
        if not visual_id or visual_id in seen:
            errors.append(f"visuals[{index}].id is missing or duplicate")
            continue
        seen.add(visual_id)
        placeholder = f"<!-- visual:{visual_id} -->"
        count = text.count(placeholder)
        if count != 1:
            errors.append(f"placeholder {visual_id} appears {count} times; expected once")
            continue
        image = Path(item.get("path", ""))
        if not image.is_absolute():
            image = mapping_path.parent / image
        if not image.is_file():
            errors.append(f"visual file does not exist: {image}")
            continue
        alt = str(item.get("alt", "")).strip()
        if not alt:
            errors.append(f"visual {visual_id} has no alt text")
            continue
        target = os.path.relpath(image.resolve(), output.parent.resolve()).replace(os.sep, "/")
        replacement = f"![{alt}](<{target}>)"
        caption = str(item.get("caption", "")).strip()
        if caption:
            replacement += f"\n\n_{caption}_"
        text = text.replace(placeholder, replacement)
    leftovers = [line.strip() for line in text.splitlines() if "<!-- visual:" in line]
    if leftovers:
        errors.append("unresolved visual placeholders remain: " + ", ".join(leftovers))
    return errors, text


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--draft", required=True, type=Path)
    parser.add_argument("--mapping", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    for path in (args.draft, args.mapping):
        if not path.is_file():
            print(f"error: file does not exist: {path}", file=sys.stderr)
            return 2
    try:
        errors, text = assemble(args.draft.resolve(), args.mapping.resolve(), args.out.resolve())
    except (OSError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 2
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(text, encoding="utf-8")
    print(f"Assembled Markdown: {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
