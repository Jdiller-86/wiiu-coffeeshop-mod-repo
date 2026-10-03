# Wii U CoffeeShop Picks

A community catalog for [CoffeeShop](https://github.com/timkicker/coffeeshop), the Wii U SDCafiine mod manager. The live feed currently has **14 archive-checked mods across five Wii U games**. It includes character skins, level hacks, a Splatoon expansion, and a Breath of the Wild quest change.

The repository contains metadata only. ZIPs are downloaded from the mod creators or existing community hosts. See [SOURCES.md](SOURCES.md) for attribution and [DISCOVERY.md](DISCOVERY.md) for notable projects that need manual installation or a different archive layout.

## Add this repository to CoffeeShop

1. Install [Aroma](https://aroma.foryour.cafe/) and [CoffeeShop](https://github.com/timkicker/coffeeshop#installation) on your Wii U. CoffeeShop uses SDCafiine for loading installed game files.
2. On the SD card, create or open **`SD:/wiiu/apps/coffeeshop/config.json`**. Copy [config.example.json](config.example.json) if you do not already have a config file.
3. Put this exact raw index URL in its `repos` array:

   ```json
   {
     "repos": [
       "https://raw.githubusercontent.com/Jdiller-86/wiiu-coffeeshop-mod-repo/main/repo.json"
     ]
   }
   ```

4. If you already use another repository, keep its URL and add ours as another array item, separated by a comma:

   ```json
   {
     "repos": [
       "https://raw.githubusercontent.com/another-owner/another-repo/main/repo.json",
       "https://raw.githubusercontent.com/Jdiller-86/wiiu-coffeeshop-mod-repo/main/repo.json"
     ]
   }
   ```

5. Safely eject the SD card, launch CoffeeShop, and browse the game list. If you just edited the file while CoffeeShop was open, restart the app or refresh its repository data in Settings.

Use the **raw `repo.json` URL**, not the GitHub repository page URL. CoffeeShop's [official configuration reference](https://github.com/timkicker/coffeeshop#configjson-reference) supports multiple repositories.

## Live catalog

| Game | Mods | Highlights |
| --- | ---: | --- |
| Mario Kart 8 | 6 | Squidward, SpongeBob, Shrek, Dr. Doofenshmirtz, Crewmate+, Hotel Mario |
| Splatoon | 3 | Splatoon+, Squidward Expansion, Sunset Maps |
| New Super Mario Bros. U | 3 | Cloudy SMBU 2, Floor Is Lava, Snowy SMBU |
| Super Mario 3D World | 1 | 3D Land 4-3 |
| Breath of the Wild | 1 | Korok Trials before Master Sword |

The three New Super Mario Bros. U total conversions are alternatives. Install and activate one at a time. **Splatoon+ needs NoHash and Rival Unpatched**, which CoffeeShop does not install for you; follow the [creator's instructions](https://gamebanana.com/mods/570597) and use the `Player.pack` included with Splatoon+. CoffeeShop may report file conflicts when mods change the same files; review those before activation.

Some mod archives are large: Cloudy SMBU 2 and Floor Is Lava are each about 0.9 GB. Leave enough free SD card space for both the downloaded ZIP and extracted files. ZIPs include extra documentation or metadata in a few cases, but every listed archive has game files directly under a top-level `content/` directory.

### Match the full Title ID

CoffeeShop asks which region to install under when a game has multiple Title IDs. Match the **full ID** for your copy of the game; a region label in the current app may be inaccurate.

| Game | USA | Europe | Japan |
| --- | --- | --- | --- |
| Mario Kart 8 | `000500001010EC00` | `000500001010ED00` | `000500001010EB00` |
| Splatoon | `0005000010176900` | `0005000010176A00` | `0005000010162B00` |
| New Super Mario Bros. U | `0005000010101D00` | `0005000010101E00` | `0005000010101C00` |
| Super Mario 3D World | `0005000010145C00` | `0005000010145D00` | `0005000010106100` |
| Breath of the Wild | `00050000101C9400` | `00050000101C9500` | `00050000101C9300` |

These are the base game's IDs from the [WiiUBrew title database](https://wiiubrew.org/wiki/Title_database); update and DLC IDs are different. The separate **New Super Mario Bros. U + New Super Luigi U** bundle also has different IDs and is not listed here. A mod may use region-specific language assets; check its source page before installing outside the creator's tested region.

## How this feed was checked

The catalog follows the [official CoffeeShop repository format](https://github.com/timkicker/coffeeshop-repo-template): a version 1 `repo.json` with relative paths to each game's `game.json`, plus HTTPS ZIP downloads. On **2026-10-03**, every listed ZIP was downloaded and checked for a root `content/` folder. Its measured size and SHA-256 are pinned in the game JSON, so CoffeeShop rejects a changed download until the catalog is reviewed and updated. These checks establish archive format and integrity; they are not a claim that every mod was tested on a physical Wii U or in every region.

Run the local validator before a change:

```sh
python validate.py
python validate.py --check-urls
python validate.py --check-archives
```

`--check-archives` downloads every ZIP again and uses several gigabytes of temporary disk space and bandwidth. GitHub Actions runs the structural validator on pushes and pull requests. See [CONTRIBUTING.md](CONTRIBUTING.md) before proposing another mod.

## Sources and distribution

This repository does not host or claim ownership of any mod binary. Some downloads are from existing CoffeeShop repositories whose maintainers adjusted ZIP layout for direct installation; the original mod pages and those hosts are linked in [SOURCES.md](SOURCES.md). Licenses are intentionally omitted from the feed unless verified from the creator. If an author wants an entry changed or removed, open an issue with the mod name and original page.
