#!/usr/bin/env python3
"""Validate this CoffeeShop feed and optionally re-audit its remote archives."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import tempfile
import urllib.error
import urllib.request
import zipfile
from pathlib import Path, PurePosixPath
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parent
ID_RE = re.compile(r"^[a-z0-9][a-z0-9_-]*$")
TITLE_RE = re.compile(r"^00050000[0-9A-F]{8}$")
SHA_RE = re.compile(r"^[0-9a-f]{64}$")
SUPPORTED_METHODS = {zipfile.ZIP_STORED, zipfile.ZIP_DEFLATED}
USER_AGENT = "WiiU-CoffeeShop-Picks-Validator/1.0"


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def https_url(value: object) -> bool:
    if not isinstance(value, str):
        return False
    parsed = urlparse(value)
    return parsed.scheme == "https" and bool(parsed.netloc) and not parsed.username


def load_json(path: Path, errors: list[str]) -> dict | None:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        errors.append(f"{path.relative_to(ROOT)}: {exc}")
        return None
    if not isinstance(value, dict):
        errors.append(f"{path.relative_to(ROOT)}: expected a JSON object")
        return None
    return value


def validate_feed() -> tuple[list[dict], list[str]]:
    errors: list[str] = []
    mods: list[dict] = []
    index = load_json(ROOT / "repo.json", errors)
    if index is None:
        return mods, errors

    require(index.get("formatVersion") == 1, "repo.json: formatVersion must be 1", errors)
    for field in ("name", "description", "author", "version"):
        require(isinstance(index.get(field), str) and bool(index[field].strip()),
                f"repo.json: {field} must be a nonempty string", errors)
    entries = index.get("games")
    if not isinstance(entries, list) or not entries:
        errors.append("repo.json: games must be a nonempty list")
        return mods, errors

    seen_games: set[str] = set()
    seen_mods: set[str] = set()
    for entry in entries:
        if not isinstance(entry, dict):
            errors.append("repo.json: each game entry must be an object")
            continue
        game_id, path_value = entry.get("id"), entry.get("path")
        if not isinstance(game_id, str) or not ID_RE.fullmatch(game_id):
            errors.append(f"repo.json: invalid game id {game_id!r}")
            continue
        if game_id in seen_games:
            errors.append(f"repo.json: duplicate game id {game_id}")
        seen_games.add(game_id)
        if (not isinstance(path_value, str) or "\\" in path_value
                or PurePosixPath(path_value).is_absolute()
                or ".." in PurePosixPath(path_value).parts
                or not path_value.startswith("games/")
                or not path_value.endswith("/game.json")):
            errors.append(f"repo.json: unsafe game path {path_value!r}")
            continue
        path = ROOT / path_value
        game = load_json(path, errors)
        if game is None:
            continue
        context = path_value
        require(isinstance(game.get("name"), str) and bool(game["name"].strip()),
                f"{context}: name must be a nonempty string", errors)
        title_ids = game.get("titleIds")
        if not isinstance(title_ids, list) or not title_ids:
            errors.append(f"{context}: titleIds must be a nonempty list")
        else:
            for title_id in title_ids:
                require(isinstance(title_id, str) and bool(TITLE_RE.fullmatch(title_id)),
                        f"{context}: invalid base-game title ID {title_id!r}", errors)
            require(len(title_ids) == len(set(str(x) for x in title_ids)),
                    f"{context}: duplicate title ID", errors)
        if "icon" in game:
            require(https_url(game["icon"]), f"{context}: icon must be an HTTPS URL", errors)
        game_mods = game.get("mods")
        if not isinstance(game_mods, list) or not game_mods:
            errors.append(f"{context}: mods must be a nonempty list")
            continue
        for mod in game_mods:
            if not isinstance(mod, dict):
                errors.append(f"{context}: each mod must be an object")
                continue
            mod_id = mod.get("id")
            label = f"{context} / {mod_id or '?'}"
            require(isinstance(mod_id, str) and bool(ID_RE.fullmatch(mod_id)),
                    f"{label}: invalid mod id", errors)
            if isinstance(mod_id, str):
                require(mod_id not in seen_mods, f"{label}: duplicate global mod id", errors)
                seen_mods.add(mod_id)
            for field in ("name", "author", "version", "description"):
                require(isinstance(mod.get(field), str) and bool(mod[field].strip()),
                        f"{label}: {field} must be a nonempty string", errors)
            require(mod.get("type") in ("mod", "modpack"),
                    f"{label}: type must be mod or modpack", errors)
            require(https_url(mod.get("download")), f"{label}: download must be HTTPS", errors)
            size = mod.get("fileSize")
            require(type(size) is int and size > 0,
                    f"{label}: fileSize must be a positive byte count", errors)
            sha = mod.get("sha256")
            require(isinstance(sha, str) and bool(SHA_RE.fullmatch(sha)),
                    f"{label}: sha256 must be 64 lowercase hex digits", errors)
            for field in ("thumbnail",):
                if field in mod:
                    require(https_url(mod[field]), f"{label}: {field} must be HTTPS", errors)
            for field in ("screenshots", "tags", "requirements"):
                if field in mod:
                    values = mod[field]
                    require(isinstance(values, list) and all(
                        isinstance(x, str) and x.strip() for x in values),
                        f"{label}: {field} must be a list of nonempty strings", errors)
                    if field == "screenshots" and isinstance(values, list):
                        require(all(https_url(x) for x in values),
                                f"{label}: screenshots must be HTTPS URLs", errors)
            mods.append(mod)
    return mods, errors


def request(url: str, method: str = "GET"):
    return urllib.request.Request(url, method=method, headers={"User-Agent": USER_AGENT})


def check_url(mod: dict) -> str | None:
    try:
        with urllib.request.urlopen(request(mod["download"], "HEAD"), timeout=30) as response:
            if response.status >= 400:
                return f"{mod['id']}: HTTP {response.status}"
    except urllib.error.HTTPError as exc:
        if exc.code != 405:
            return f"{mod['id']}: HTTP {exc.code}"
        try:
            ranged = urllib.request.Request(mod["download"], headers={
                "User-Agent": USER_AGENT, "Range": "bytes=0-0"})
            with urllib.request.urlopen(ranged, timeout=30):
                pass
        except (OSError, urllib.error.URLError) as retry_exc:
            return f"{mod['id']}: {retry_exc}"
    except (OSError, urllib.error.URLError) as exc:
        return f"{mod['id']}: {exc}"
    return None


def check_archive(mod: dict) -> str | None:
    import os

    fd, filename = tempfile.mkstemp(prefix="coffeeshop-audit-", suffix=".zip")
    os.close(fd)
    try:
        sha = hashlib.sha256()
        count = 0
        with urllib.request.urlopen(request(mod["download"]), timeout=120) as response:
            if response.status >= 400:
                return f"{mod['id']}: HTTP {response.status}"
            with open(filename, "wb") as output:
                while chunk := response.read(1024 * 1024):
                    output.write(chunk)
                    sha.update(chunk)
                    count += len(chunk)
        if count != mod["fileSize"]:
            return f"{mod['id']}: size changed ({count} vs {mod['fileSize']})"
        if sha.hexdigest() != mod["sha256"]:
            return f"{mod['id']}: SHA-256 mismatch"
        with zipfile.ZipFile(filename) as archive:
            files = [item for item in archive.infolist() if not item.is_dir()]
            if not files:
                return f"{mod['id']}: empty ZIP"
            if not any(item.filename.startswith(("content/", "aoc/")) for item in files):
                return f"{mod['id']}: no files under a root content/ or aoc/ directory"
            for item in archive.infolist():
                path = PurePosixPath(item.filename)
                if (not path.parts or item.filename.startswith("/")
                        or "\\" in item.filename or ".." in path.parts
                        or ":" in path.parts[0]):
                    return f"{mod['id']}: unsafe ZIP path {item.filename!r}"
                if item.flag_bits & 1:
                    return f"{mod['id']}: encrypted ZIP entry {item.filename!r}"
                if item.compress_type not in SUPPORTED_METHODS:
                    return f"{mod['id']}: unsupported ZIP method on {item.filename!r}"
    except (OSError, urllib.error.URLError, zipfile.BadZipFile) as exc:
        return f"{mod['id']}: {exc}"
    finally:
        os.unlink(filename)
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check-urls", action="store_true", help="HEAD check every download URL")
    parser.add_argument("--check-archives", action="store_true",
                        help="download every ZIP to check size, SHA-256 and root layout (several GB)")
    parser.add_argument("--mod", metavar="ID", help="limit network checks to one mod ID")
    args = parser.parse_args()
    mods, errors = validate_feed()
    if args.mod:
        mods = [mod for mod in mods if mod.get("id") == args.mod]
        if not mods:
            errors.append(f"unknown mod ID: {args.mod}")
    if not errors and args.check_urls:
        errors.extend(filter(None, (check_url(mod) for mod in mods)))
    if not errors and args.check_archives:
        for mod in mods:
            print(f"Auditing {mod['id']}...", flush=True)
            issue = check_archive(mod)
            if issue:
                errors.append(issue)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"Valid CoffeeShop v1 feed: {len(mods)} mod(s) checked")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
