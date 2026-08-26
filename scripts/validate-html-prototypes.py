#!/usr/bin/env python3
"""Validate the static-first HTML/SVG prototype examples.

This is intentionally a small, dependency-free guardrail for the handoff contract:
all declared prototype states must be present in the initial HTML DOM, each state
must contain an accessible inline SVG, and JavaScript cannot be the only renderer.
It does not replace browser or visual QA.
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_GLOB = "skills/pm-prd-html/examples/*.html"
ERRORS: list[str] = []


def error(path: Path, message: str) -> None:
    ERRORS.append(f"{path.relative_to(ROOT)}: {message}")


def attr(tag: str, name: str) -> str | None:
    match = re.search(rf"\b{name}=(?:\"([^\"]*)\"|'([^']*)')", tag, re.I)
    return (match.group(1) or match.group(2)) if match else None


def validate_file(path: Path) -> None:
    text = path.read_text(encoding="utf-8")

    # Static-first contract: no runtime HTML injection or external source loading.
    for forbidden in ("innerHTML", "outerHTML", "document.write", "insertAdjacentHTML"):
        if forbidden in text:
            error(path, f"forbidden runtime HTML injection token: {forbidden}")
    if re.search(r"<(?:script|link)\b[^>]+\bsrc=|<link\b[^>]+\bhref=\s*['\"]https?://", text, re.I):
        error(path, "external script/style resource is not allowed")
    if re.search(r"<img\b[^>]+\bsrc=\s*['\"]https?://", text, re.I):
        error(path, "external image resource is not allowed")
    if re.search(r"@import\s+(?:url\()?\s*['\"]?https?://", text, re.I):
        error(path, "external CSS import is not allowed")
    if re.search(r"url\(\s*['\"]?https?://", text, re.I):
        error(path, "external CSS URL is not allowed")

    state_ids = re.findall(r'<(?:a|button)\b[^>]*\bdata-state=["\']([^"\']+)', text, re.I)
    article_ids = re.findall(r'<article\b[^>]*\bclass=["\'][^"\']*prototype-state[^"\']*["\'][^>]*\bdata-state=["\']([^"\']+)', text, re.I)
    # Attribute order can vary in authored HTML; use a second broad match as fallback.
    if not article_ids:
        article_ids = re.findall(r'<article\b(?=[^>]*\bclass=["\'][^"\']*prototype-state)(?=[^>]*\bdata-state=["\']([^"\']+))[^>]*>', text, re.I)

    if not state_ids:
        error(path, "no prototype navigation states found")
        return
    if not article_ids:
        error(path, "no static .prototype-state articles found")
        return
    if set(state_ids) != set(article_ids):
        error(path, f"navigation/article state mismatch: nav={sorted(set(state_ids))}, articles={sorted(set(article_ids))}")
    if len(article_ids) != len(set(article_ids)):
        error(path, "prototype state IDs are not unique")

    svg_matches = list(re.finditer(r"<svg\b[^>]*>.*?</svg>", text, re.I | re.S))
    if len(svg_matches) < len(article_ids):
        error(path, f"only {len(svg_matches)} inline SVGs for {len(article_ids)} prototype states")

    node_ids: list[str] = []
    for index, match in enumerate(svg_matches, start=1):
        opening = re.search(r"<svg\b[^>]*>", match.group(0), re.I | re.S)
        opening_tag = opening.group(0) if opening else ""
        state = attr(opening_tag, "data-node-id") or f"svg-{index}"
        node_ids.append(state)
        if not attr(opening_tag, "viewBox"):
            error(path, f"SVG {state} is missing viewBox")
        if attr(opening_tag, "role") != "img":
            error(path, f"SVG {state} must declare role=img")
        if not re.search(r"<title\b[^>]*>.*?</title>", match.group(0), re.I | re.S):
            error(path, f"SVG {state} is missing title")
        if not re.search(r"<desc\b[^>]*>.*?</desc>", match.group(0), re.I | re.S):
            error(path, f"SVG {state} is missing desc")
        if not attr(opening_tag, "data-node-id"):
            error(path, f"SVG {state} is missing stable data-node-id")
        svg_text = match.group(0)
        if re.search(r"<script\b|<foreignObject\b", svg_text, re.I):
            error(path, f"SVG {state} contains a forbidden script or foreignObject")
        if re.search(r"\son[a-z][a-z0-9_-]*\s*=", svg_text, re.I):
            error(path, f"SVG {state} contains a forbidden event handler")
        if re.search(r"(?:href|xlink:href)\s*=\s*['\"](?:https?:|file:|data:)", svg_text, re.I):
            error(path, f"SVG {state} references a non-local resource")
        try:
            ET.fromstring(match.group(0))
        except ET.ParseError as exc:
            error(path, f"SVG {state} is not valid XML: {exc}")

    if len(node_ids) != len(set(node_ids)):
        error(path, "SVG data-node-id values are not unique")
    if set(article_ids) != set(node_ids):
        error(path, f"prototype state/SVG node mismatch: states={sorted(set(article_ids))}, svgNodes={sorted(set(node_ids))}")

    # Every static prototype article must have an SVG before any script executes.
    for state in article_ids:
        article_match = re.search(
            rf'<article\b(?=[^>]*\bdata-state=["\']{re.escape(state)}["\'])[^>]*>.*?</article>',
            text,
            re.I | re.S,
        )
        if not article_match or not re.search(r"<svg\b", article_match.group(0), re.I):
            error(path, f"state {state} has no inline SVG in initial DOM")

    # Syntax-check authored scripts when Node is available. This catches accidental
    # breakage while keeping the validator usable in minimal environments.
    node = shutil.which("node")
    if node:
        scripts = re.findall(r"<script\b[^>]*>(.*?)</script>", text, re.I | re.S)
        for index, script in enumerate(scripts, start=1):
            with tempfile.NamedTemporaryFile("w", suffix=".js", encoding="utf-8") as handle:
                handle.write(script)
                handle.flush()
                result = subprocess.run([node, "--check", handle.name], capture_output=True, text=True)
            if result.returncode:
                error(path, f"script {index} failed node --check: {result.stderr.strip()}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="*", type=Path, help="HTML files; defaults to prototype examples")
    args = parser.parse_args()
    paths = args.paths or sorted(ROOT.glob(DEFAULT_GLOB))
    if not paths:
        print("ERROR: no HTML prototype examples found", file=sys.stderr)
        return 1
    for path in paths:
        validate_file(path if path.is_absolute() else ROOT / path)
    if ERRORS:
        print("HTML prototype validation failed:", file=sys.stderr)
        print("\n".join(f"- {item}" for item in ERRORS), file=sys.stderr)
        return 1
    print(f"Validated {len(paths)} static-first HTML prototype examples.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
