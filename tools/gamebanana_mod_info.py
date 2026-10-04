#!/usr/bin/env python3
"""Print creator and description metadata for public GameBanana mod IDs."""

from __future__ import annotations

import argparse
import html
from html.parser import HTMLParser
import json
import urllib.parse
import urllib.request


class PlainText(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []

    def handle_data(self, data: str) -> None:
        self.parts.append(data)

    def text(self) -> str:
        return " ".join(" ".join(self.parts).split())


def fetch(mod_id: int) -> dict:
    query = urllib.parse.urlencode({
        "itemtype": "Mod", "itemid": mod_id,
        "fields": "name,Owner().name,Credits().ssvAuthorNames(),text,install_instructions",
        "return_keys": "1",
    })
    request = urllib.request.Request(
        "https://api.gamebanana.com/Core/Item/Data?" + query,
        headers={"User-Agent": "Mozilla/5.0"},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        data = json.load(response)
    parser = PlainText()
    parser.feed(html.unescape(data.get("text") or ""))
    data["text"] = parser.text()
    return data


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mod_ids", type=int, nargs="+")
    args = parser.parse_args()
    for mod_id in args.mod_ids:
        print(json.dumps({"mod_id": mod_id, **fetch(mod_id)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
