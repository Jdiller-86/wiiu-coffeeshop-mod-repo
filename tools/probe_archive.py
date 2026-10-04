#!/usr/bin/env python3
"""Inspect a candidate CoffeeShop ZIP before adding it to the feed.

Downloads into a temporary file, prints the measured size and SHA-256, and
checks whether SDCafiine game files are at the archive root. The temporary
copy is always removed.
"""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import json
import os
import sys
import tempfile
import time
import urllib.request
import zipfile
from pathlib import PurePosixPath
from urllib.parse import urlsplit, urlunsplit


def probe(url: str, max_bytes: int) -> dict:
    request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    fd, path = tempfile.mkstemp(prefix="coffeeshop-probe-", suffix=".zip")
    os.close(fd)
    result: dict = {"url": url}
    try:
        digest = hashlib.sha256()
        size = 0
        started = time.monotonic()
        with urllib.request.urlopen(request, timeout=20) as response, open(path, "wb") as output:
            # Release hosts often redirect to short-lived signed URLs. Keep the
            # host and path for troubleshooting without printing query tokens.
            parts = urlsplit(response.url)
            result["resolved_url"] = urlunsplit((parts.scheme, parts.netloc, parts.path, "", ""))
            declared = response.headers.get("Content-Length")
            if declared and int(declared) > max_bytes:
                raise ValueError(f"declared size {declared} exceeds {max_bytes} byte limit")
            while chunk := response.read(1024 * 1024):
                if time.monotonic() - started > 180:
                    raise TimeoutError("download exceeded three-minute audit limit")
                size += len(chunk)
                if size > max_bytes:
                    raise ValueError(f"download exceeds {max_bytes} byte limit")
                output.write(chunk)
                digest.update(chunk)
        result["fileSize"] = size
        result["sha256"] = digest.hexdigest()
        with zipfile.ZipFile(path) as archive:
            files = [item for item in archive.infolist() if not item.is_dir()]
            result["file_count"] = len(files)
            result["root_entries"] = sorted({item.filename.split("/")[0] for item in files})[:30]
            result["sample_paths"] = [item.filename for item in files[:8]]
            result["root_content_or_aoc"] = any(
                item.filename.startswith(("content/", "aoc/")) for item in files
            )
            result["unsafe_paths"] = [
                item.filename for item in files if (
                    item.filename.startswith("/")
                    or "\\" in item.filename
                    or ".." in PurePosixPath(item.filename).parts
                    or ":" in PurePosixPath(item.filename).parts[0]
                )
            ][:10]
            result["encrypted"] = any(item.flag_bits & 1 for item in files)
            result["unsupported_methods"] = sorted({
                item.compress_type for item in files
                if item.compress_type not in (zipfile.ZIP_STORED, zipfile.ZIP_DEFLATED)
            })
        return result
    finally:
        os.unlink(path)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("urls", nargs="+", help="direct HTTPS ZIP URLs")
    parser.add_argument("--max-mb", type=int, default=2000,
                        help="maximum downloaded size in decimal MB (default: 2000)")
    parser.add_argument("--workers", type=int, default=3,
                        help="concurrent downloads when probing multiple ZIPs")
    parser.add_argument("--summary", action="store_true",
                        help="print one compact JSON object per URL")
    args = parser.parse_args()
    if any(not url.startswith("https://") for url in args.urls):
        parser.error("every URL must use HTTPS")

    def attempt(url: str) -> dict:
        try:
            return probe(url, args.max_mb * 1_000_000)
        except (OSError, ValueError, zipfile.BadZipFile) as exc:
            return {"url": url, "error": str(exc)}

    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {pool.submit(attempt, url): url for url in args.urls}
        results = []
        for future in as_completed(futures):
            result = future.result()
            results.append(result)
            if args.summary:
                print(json.dumps({key: result.get(key) for key in (
                    "url", "fileSize", "sha256", "root_content_or_aoc", "root_entries",
                    "unsafe_paths", "encrypted", "unsupported_methods", "error"
                ) if key in result}), flush=True)
    if not args.summary:
        print(json.dumps(results[0] if len(results) == 1 else results, indent=2))
    if any("error" in result for result in results):
        sys.exit(1)


if __name__ == "__main__":
    main()
