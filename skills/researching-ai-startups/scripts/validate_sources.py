#!/usr/bin/env python3
"""Validate portable source metadata for AI startup research."""

from __future__ import annotations

import argparse
import ipaddress
import json
import re
import sys
from datetime import date
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
NONEMPTY_STRING_FIELDS = {"id", "title", "publisher", "published_at", "media_type"}
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


def url_uses_private_host(value: object) -> bool:
    if not isinstance(value, str):
        return False
    host = urlparse(value).hostname
    if not host:
        return False
    if host.lower() == "localhost":
        return True
    try:
        return not ipaddress.ip_address(host).is_global
    except ValueError:
        return False


def validate_url(value: object, path: str) -> list[str]:
    if not isinstance(value, str) or not is_http_url(value):
        return [f"{path}: must be an HTTP or HTTPS URL"]
    parsed = urlparse(value)
    errors = []
    if parsed.username is not None or parsed.password is not None:
        errors.append(f"{path}: URL credentials are not allowed")
    if url_uses_private_host(value):
        errors.append(f"{path}: private or local URL is not portable")
    host = (parsed.hostname or "").lower()
    url_path = parsed.path.rstrip("/") or "/"
    is_youtube_search = host in {"youtube.com", "www.youtube.com", "youtu.be"} and url_path == "/results"
    is_google_search = (host == "google.com" or host.endswith(".google.com")) and url_path == "/search"
    is_bing_search = (host == "bing.com" or host.endswith(".bing.com")) and url_path == "/search"
    is_duckduckgo_search = host in {"duckduckgo.com", "www.duckduckgo.com"} and url_path == "/" and bool(parsed.query)
    if is_youtube_search or is_google_search or is_bing_search or is_duckduckgo_search:
        errors.append(f"{path}: search-results URL is not canonical evidence")
    return errors


def contains_private_ipv4(text: str) -> bool:
    for candidate in re.findall(r"(?<![\d.])(?:\d{1,3}\.){3}\d{1,3}(?![\d.])", text):
        try:
            if not ipaddress.ip_address(candidate).is_global:
                return True
        except ValueError:
            continue
    return False


def contains_private_value(value: str) -> bool:
    lowered = value.lower()
    home_path = bool(re.search(r"^/(?:root|users|home)/", lowered))
    return home_path or any(marker in lowered for marker in PRIVATE_MARKERS) or contains_private_ipv4(value)


def walk_values(value: object, path: str):
    if isinstance(value, dict):
        for key, child in value.items():
            yield from walk_values(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from walk_values(child, f"{path}[{index}]")
    else:
        yield path, value


def validate_source(source: object, index: int) -> list[str]:
    prefix = f"source[{index}]"
    if not isinstance(source, dict):
        return [f"{prefix}: source must be an object"]

    errors: list[str] = []
    for field in sorted(REQUIRED_FIELDS - source.keys()):
        errors.append(f"{prefix}: missing required field: {field}")

    for field in sorted(NONEMPTY_STRING_FIELDS):
        if field in source and (not isinstance(source[field], str) or not source[field].strip()):
            errors.append(f"{prefix}.{field}: must be a non-empty string")

    published_at = source.get("published_at")
    if isinstance(published_at, str) and published_at.strip():
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", published_at):
            errors.append(f"{prefix}.published_at: must use YYYY-MM-DD format")
        else:
            try:
                date.fromisoformat(published_at)
            except ValueError:
                errors.append(f"{prefix}.published_at: must be a valid calendar date")

    if "url" in source:
        errors.extend(validate_url(source["url"], f"{prefix}.url"))

    speakers = source.get("speakers")
    if speakers is not None and (
        not isinstance(speakers, list)
        or not speakers
        or not all(isinstance(speaker, str) and speaker.strip() for speaker in speakers)
    ):
        errors.append(f"{prefix}.speakers: must be a non-empty list of names")

    transcript = source.get("transcript")
    if not isinstance(transcript, dict):
        if "transcript" in source:
            errors.append(f"{prefix}.transcript: must be an object")
        return errors

    status = transcript.get("status")
    if status not in TRANSCRIPT_STATUSES:
        errors.append(
            f"{prefix}.transcript.status: must be one of {sorted(TRANSCRIPT_STATUSES)}"
        )

    provenance = transcript.get("provenance")
    if provenance not in TRANSCRIPT_PROVENANCE:
        errors.append(
            f"{prefix}.transcript.provenance: must be one of {sorted(TRANSCRIPT_PROVENANCE)}"
        )

    language = transcript.get("language")
    if not isinstance(language, str) or not language.strip():
        errors.append(f"{prefix}.transcript.language: must be a non-empty string")

    word_count = transcript.get("word_count")
    if word_count is None:
        if status != "available":
            errors.append(
                f"{prefix}.transcript.word_count: null is allowed only when an available transcript has not been counted"
            )
    elif not isinstance(word_count, int) or isinstance(word_count, bool) or word_count < 0:
        errors.append(f"{prefix}.transcript.word_count: must be null or a nonnegative integer")
    elif status == "available" and word_count == 0:
        errors.append(
            f"{prefix}.transcript.word_count: available transcript must use null when uncounted or a positive integer when counted"
        )

    if status == "available" and provenance == "unavailable":
        errors.append(
            f"{prefix}.transcript.provenance: available transcript cannot use unavailable provenance"
        )
    if status == "unavailable" and provenance != "unavailable":
        errors.append(
            f"{prefix}.transcript.provenance: unavailable transcript must use unavailable provenance"
        )
    if status == "unavailable" and isinstance(word_count, int) and word_count != 0:
        errors.append(
            f"{prefix}.transcript.word_count: unavailable transcript must have word_count 0"
        )

    for field_path, value in walk_values(source, prefix):
        field_name = field_path.rsplit(".", 1)[-1]
        is_url_field = field_name == "url" or field_name.endswith("_url")
        if is_url_field:
            if field_path != f"{prefix}.url":
                errors.extend(validate_url(value, field_path))
            continue
        if isinstance(value, str) and contains_private_value(value):
            errors.append(f"{field_path}: private path or environment value is not portable")

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
    if not sources:
        errors.append("source metadata array must contain at least one source")

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
