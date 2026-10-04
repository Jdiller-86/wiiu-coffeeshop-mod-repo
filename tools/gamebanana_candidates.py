#!/usr/bin/env python3
"""List public GameBanana mod leads for a game; research only, not a feed generator."""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
import json
import urllib.parse
import urllib.request


def file_summary(item: dict) -> list[str]:
    query = urllib.parse.urlencode({
        "itemtype": "Mod",
        "itemid": item["_idRow"],
        "fields": "Files().aFiles()",
        "return_keys": "1",
    })
    request = urllib.request.Request(
        "https://api.gamebanana.com/Core/Item/Data?" + query,
        headers={"User-Agent": "Mozilla/5.0"},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        details = json.load(response)
    files = details.get("Files().aFiles()") or {}
    lines = []
    for file in files.values():
        lines.append(
            f"  {file['_idRow']}\t{file['_sFile']}\t"
            f"{int(file['_nFilesize']) / 1_000_000:.1f} MB\t"
            f"{file['_sDownloadUrl']}"
        )
    return lines


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("game_id", type=int, help="GameBanana game ID")
    parser.add_argument("--page", type=int, default=1)
    parser.add_argument("--limit", type=int, default=50)
    parser.add_argument("--sort", default="Generic_MostLiked")
    parser.add_argument("--files", action="store_true",
                        help="also show each mod's creator-hosted file URLs")
    args = parser.parse_args()
    query = urllib.parse.urlencode({
        "_nPage": args.page,
        "_nPerpage": args.limit,
        "_sSort": args.sort,
        "_aFilters[Generic_Game]": args.game_id,
    })
    url = "https://gamebanana.com/apiv11/Mod/Index?" + query
    request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(request, timeout=30) as response:
        data = json.load(response)
    print(f"{data['_aMetadata']['_nRecordCount']} mods found")
    records = [item for item in data["_aRecords"]
               if item.get("_aGame", {}).get("_idRow") == args.game_id]
    file_lists = []
    if args.files:
        with ThreadPoolExecutor(max_workers=6) as pool:
            file_lists = list(pool.map(file_summary, records))
    for index, item in enumerate(records):
        if item.get("_aGame", {}).get("_idRow") != args.game_id:
            continue
        print(f"{item['_idRow']}\t{item['_sName']}\t"
              f"{item.get('_nLikeCount', '?')} likes\t"
              f"{item.get('_sProfileUrl', '')}")
        if args.files:
            print("\n".join(file_lists[index]) or "  no downloadable file")


if __name__ == "__main__":
    main()
