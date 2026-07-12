#!/usr/bin/env python3
"""Validate portable source metadata for AI startup research."""

from __future__ import annotations

import argparse
import ipaddress
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

REQUIRED_FIELDS = {
    "id",
    "title",
    "speakers",
    "publisher",
    "published_at",
    "url",
    "media_type",
    "transcript",
}
TRANSCRIPT_STATUSES = {"available", "unavailable"}
TRANSCRIPT_PROVENANCE = {
    "official",
    "platform-captions",
    "publisher-transcript",
    "third-party",
    "generated",
    "unavailable",
}
PRIVATE_MARKERS = (
    "tailscale",
    "memorykit",
    "telegram",
    "chat_id",
    "bot_token",
)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate AI startup research source metadata for completeness and portability."
    )
    parser.add_argument("source_json", type=Path, help="JSON source metadata object or array")
    parser.add_argument("--json", action="store_true", help="print a machine-readable result")
    return parser.parse_args(argv)


def is_http_url(value: object) -> bool:
    if not isinstance(value, str):
        return False
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def contains_private_ipv4(text: str) -> bool:
    for candidate in re.findall(r"(?<![\d.])(?:\d{1,3}\.){3}\d{1,3}(?![\d.])", text):
        try:
            if ipaddress.ip_address(candidate).is_private:
                return True
        except ValueError:
            continue
    return False


def contains_private_path(value: object) -> bool:
    if not isinstance(value, str):
        return False
    lowered = value.lower()
    home_path = bool(re.search(r"^/(?:root|users)/", lowered))
    return home_path or any(marker in lowered for marker in PRIVATE_MARKERS) or contains_private_ipv4(value)


def validate_source(source: object, index: int) -> list[str]:
    prefix = f"source[{index}]"
    if not isinstance(source, dict):
        return [f"{prefix}: source must be an object"]

    errors: list[str] = []
    for field in sorted(REQUIRED_FIELDS - source.keys()):
        errors.append(f"{prefix}: missing required field: {field}")

    if "url" in source and not is_http_url(source["url"]):
        errors.append(f"{prefix}: url must be an HTTP or HTTPS URL")

    speakers = source.get("speakers")
    if speakers is not None and (
        not isinstance(speakers, list)
        or not speakers
        or not all(isinstance(speaker, str) and speaker.strip() for speaker in speakers)
    ):
        errors.append(f"{prefix}: speakers must be a non-empty list of names")

    transcript = source.get("transcript")
    if not isinstance(transcript, dict):
        if "transcript" in source:
            errors.append(f"{prefix}: transcript must be an object")
        return errors

    status = transcript.get("status")
    if status not in TRANSCRIPT_STATUSES:
        errors.append(
            f"{prefix}.transcript: status must be one of {sorted(TRANSCRIPT_STATUSES)}"
        )

    provenance = transcript.get("provenance")
    if provenance not in TRANSCRIPT_PROVENANCE:
        errors.append(
            f"{prefix}.transcript: provenance must be one of {sorted(TRANSCRIPT_PROVENANCE)}"
        )

    word_count = transcript.get("word_count")
    if not isinstance(word_count, int) or isinstance(word_count, bool) or word_count < 0:
        errors.append(f"{prefix}.transcript: word_count must be a nonnegative integer")

    if status == "available" and provenance == "unavailable":
        errors.append(f"{prefix}.transcript: available transcript cannot use unavailable provenance")
    if status == "unavailable" and provenance != "unavailable":
        errors.append(f"{prefix}.transcript: unavailable transcript must use unavailable provenance")

    for field, value in transcript.items():
        if contains_private_path(value):
            errors.append(f"{prefix}.transcript.{field}: private path or environment value is not portable")

    return errors


def load_sources(path: Path) -> list[object]:
    with path.open(encoding="utf-8") as handle:
        payload = json.load(handle)
    return payload if isinstance(payload, list) else [payload]


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        sources = load_sources(args.source_json)
    except (OSError, json.JSONDecodeError) as exc:
        errors = [f"cannot read source metadata: {exc}"]
        result = {"sources": 0, "errors": errors}
        print(json.dumps(result) if args.json else f"ERROR: {errors[0]}")
        return 1

    errors = [
        error
        for index, source in enumerate(sources)
        for error in validate_source(source, index)
    ]
    result = {"sources": len(sources), "errors": errors}

    if args.json:
        print(json.dumps(result, indent=2))
    elif errors:
        print(f"FAIL: {len(sources)} sources, {len(errors)} errors")
        for error in errors:
            print(f"- {error}")
    else:
        print(f"PASS: {len(sources)} sources, 0 errors")

    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
