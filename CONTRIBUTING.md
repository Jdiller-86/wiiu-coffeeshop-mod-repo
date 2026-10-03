# Adding or updating a mod

CoffeeShop shows an Install action for every entry in `game.json`, so add a mod to the live feed only when the archive can be installed directly. The [official template](https://github.com/timkicker/coffeeshop-repo-template) documents the format.

1. Find the original creator page and credit its author. Record that page and the archive host in [SOURCES.md](SOURCES.md). Prefer the creator's direct HTTPS ZIP. Do not mirror or repack someone else's mod without permission.
2. Verify that the ZIP has actual game files immediately under `content/` (or `aoc/` for applicable DLC content) **at the archive root**. A ZIP containing `some-folder/content/`, a whole `sdcafiine/` tree, a Cemu graphic pack, `.bnp`, `.rar`, `.7z`, an installer, or a source-code archive is not ready for CoffeeShop. CoffeeShop's extractor accepts stored and Deflate ZIP entries.
3. Verify the game's Wii U base Title IDs using the [WiiUBrew title database](https://wiiubrew.org/wiki/Title_database). Do not use update or DLC Title IDs. Check the creator's region and game-version requirements.
4. Add the entry in `games/<game>/game.json`, with a globally unique lowercase mod ID, author, accurate version and short description, direct HTTPS download URL, `type`, measured `fileSize`, and lowercase SHA-256. Add image and tag URLs only if they resolve. Put manual dependencies in `requirements` and the description.
5. Run `python validate.py`, `python validate.py --check-urls`, and `python validate.py --check-archives`. The last command downloads every archive and may take time. Include any limitations in the pull request.

Mods that need a desktop loader, rebuilding, archive rearrangement, or a console-specific setup belong in [DISCOVERY.md](DISCOVERY.md) until they have an authorized direct-install ZIP. Do not invent a license for a mod or assume a third-party catalog's license field is correct.
