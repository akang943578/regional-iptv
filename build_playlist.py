#!/usr/bin/env python3
"""Build a compact Asia-Pacific and English-region playlist from Free-TV."""

from __future__ import annotations

import argparse
import re
import urllib.request
from pathlib import Path

SOURCE_URL = "https://raw.githubusercontent.com/Free-TV/IPTV/master/playlist.m3u8"

# Chinese-speaking regions, nearby East/Southeast Asia, Oceania, and major
# English-speaking regions requested for this TV.
COUNTRIES = {
    "CN", "HK", "MO", "TW",
    "JP", "KR",
    "SG", "MY", "ID", "PH", "TH", "VN", "BN", "KH", "LA", "MM", "TL",
    "AU", "NZ",
    "GB", "IE", "US", "CA",
}

# Free-TV uses these visible suffixes for sources that need a web wrapper,
# are geo-blocked, or are not direct TV streams.
BLOCKED_MARKERS = ("Ⓖ", "Ⓨ", "Ⓣ")
SHOPPING_PATTERN = re.compile(
    r"(?i)\b(shopping|shop\s*channel|qvc|tvsn|gems\s*tv|tjc|hobby\s*maker)\b"
)
COUNTRY_PATTERN = re.compile(r'tvg-country="([^"]*)"')
ID_PATTERN = re.compile(r'tvg-id="([^"]*)"')


def download(url: str) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": "regional-iptv-builder/1"})
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read().decode("utf-8-sig", errors="replace")


def entries(text: str):
    lines = text.splitlines()
    index = 0
    while index < len(lines):
        if not lines[index].startswith("#EXTINF:"):
            index += 1
            continue

        info = lines[index].strip()
        extra = []
        index += 1
        while index < len(lines) and not lines[index].startswith("#EXTINF:"):
            line = lines[index].strip()
            index += 1
            if not line:
                continue
            if line.startswith("#"):
                extra.append(line)
                continue
            yield info, extra, line
            break


def build(text: str) -> tuple[str, int]:
    output = ["#EXTM3U"]
    seen = set()
    count = 0

    for info, extra, url in entries(text):
        country_match = COUNTRY_PATTERN.search(info)
        countries = set(country_match.group(1).split(";")) if country_match else set()
        if not countries.intersection(COUNTRIES):
            continue
        if any(marker in info for marker in BLOCKED_MARKERS):
            continue
        if SHOPPING_PATTERN.search(info):
            continue
        if not url.startswith(("http://", "https://")):
            continue

        id_match = ID_PATTERN.search(info)
        key = id_match.group(1) if id_match and id_match.group(1) else url
        if key in seen:
            continue
        seen.add(key)

        output.extend((info, *extra, url))
        count += 1

    return "\n".join(output) + "\n", count


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", default=SOURCE_URL)
    parser.add_argument("--output", default="playlist.m3u8")
    args = parser.parse_args()

    source = Path(args.source).read_text(encoding="utf-8") if Path(args.source).exists() else download(args.source)
    playlist, count = build(source)
    Path(args.output).write_text(playlist, encoding="utf-8")
    print(f"Wrote {count} channels to {args.output}")


if __name__ == "__main__":
    main()
