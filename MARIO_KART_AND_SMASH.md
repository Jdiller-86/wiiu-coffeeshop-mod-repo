# Large Mario Kart 8 and Smash Wii U mods

Researched 2026-10-04. These are Wii U projects worth exploring **outside the installable CoffeeShop feed**. The live feed already has [35 Mario Kart 8 mods](MOD_LIST.md#mario-kart-8-35-mods), including custom tracks and joke characters. A pack can enter the feed only when its creator or authorized host offers one direct HTTPS ZIP with playable files under root `content/` and/or `aoc/`, plus a clear Wii U region and version. CoffeeShop installs files but does not select variants, merge Smash files, or install a code loader.

## Mario Kart 8

| Pack | Why it is interesting | CoffeeShop status |
| --- | --- | --- |
| [CTGP-Universe Zeta](https://gamebanana.com/mods/49460) | 17 custom tracks, music, cup icons and menus. | The creator's roughly 702 MB ZIP begins with `CTGP-U Zeta/`, so a direct feed entry would extract one level too deep. Follow the creator's manual installation steps. |
| [Mario Kart Generations](https://gamebanana.com/wips/68919) | Custom menus, music, characters and 48 replacement tracks. | The GameBanana project is a WiP page without a direct mod ZIP; its distribution and setup are separate. Use the project's current release instructions. |
| [Mario Kart Universal](https://gamebanana.com/mods/508408) | Broad track, character, kart, UI and music changes. The creator lists a **Lite v1.0** specifically for real Wii U hardware. | Its GameBanana file is a 112-byte pointer to external downloads, not the mod. Use the creator's Lite download and instructions; run it alone. |
| [Mario Kart 8 Ultimate](https://gbatemp.net/threads/mario-kart-8-ultimate-download-the-alpha-now-104-additional-courses-to-the-base-game.582921/) | Creator's alpha adds 104 courses beside the original courses. | The creator's setup uses a separate track expansion/code-loading framework and region-specific steps. CoffeeShop cannot install that framework as a normal SDCafiine ZIP. |
| [Mario Kart 8 Deluxe Modpack](https://gamebanana.com/mods/49464) | Brings Deluxe-inspired characters and presentation to the Wii U game. | The GameBanana download is a tiny readme; the creator says to apply v4.2.1 over v4.0 and choose console-specific options. It is a manual multi-step install. |

For an immediate CoffeeShop install, the [Mario Kart 8 live list](MOD_LIST.md#mario-kart-8-35-mods) includes Luigi Circuit, Sky Arena, Ninja Hideaway, Vancouver Velocity, Broken Rainbow Road, Rosalina's Crystal Lagoon and several other courses. These replace existing course slots, so review conflicts when enabling them together.

## Super Smash Bros. for Wii U

**Project M and Project+ are mods for *Super Smash Bros. Brawl* on Wii.** They can be played through a Wii U's vWii mode, but do not modify the native Wii U Smash game. For Smash Wii U, the closest gameplay direction is [Melee HD](https://videogamemods.com/mastaklo-mods/super-smash-bros/mods/melee-hd), an early 4XM-related release, or the other Smash 4 overhauls below. The published downloads require manual setup; none of the checked files is a direct CoffeeShop entry.

| Pack | Why it is interesting | CoffeeShop status |
| --- | --- | --- |
| [Melee HD](https://videogamemods.com/mastaklo-mods/super-smash-bros/mods/melee-hd) | Melee-inspired movement, movesets and mechanics for Smash Wii U. | Creator offers packed, unpacked and PAL variants through MEGA. Select a region and use the creator's installation instructions. |
| [Sm4sh Remix Phase 3](https://gamebanana.com/mods/48799) | Roster rebalance, new moves, shield dropping and more offensive play. | Packed and unpacked ZIPs, plus a separate EU variant, have patch/variant layouts rather than one root `content/` mod. |
| [TR4SH v1.10.5](https://gamebanana.com/mods/48602) | A large, deliberately silly overhaul of all 58 fighters, plus music, voices, UI and stage-hazard options. | The US download is a roughly 928 MB `.rar`; EU and JP releases are separate. Install the right region manually. |
| [CH4OS: Forever Unbalanced](https://gamebanana.com/mods/48810) | Wildly overpowered fighters and moves meant for chaotic matches with friends. | The GameBanana ZIP contains logos and images only; the creator points to an alternate large mod download and its own setup. |
| [Smash Rebuffed v2.5C](https://gamebanana.com/mods/48794) | Faster, more offensive gameplay with overhauled fighter moves and balance. | The main download is an unpacked `.7z`; the creator supplies packed builds separately, including an EU option. |
| [Project M Character Param for Smash 4](https://gamebanana.com/mods/48607) | Gives Smash 4 fighters Project M-like movement and combat parameters. | The ZIP starts with `Project M Param/`; the creator directs users to place files under their region's `data/param/fighter` path. |
| [B4lanced v0.3](https://gamebanana.com/mods/48608) | Another broad Smash 4 balance option. | The checked ZIP starts with `b4lanced_v03/`, requiring manual selection and placement. |
| [Training Modpack v3.5](https://gamebanana.com/mods/48370) | Save states, DI practice, hitbox visualization and training toggles. | Bundles full, training-only, packed and unpacked variants. Choose and install the correct one using the creator's steps. |
| [The (Melee) Hybrid Modpack](https://gamebanana.com/mods/48598) | Melee-inspired Roy and Marth plus Brawl-inspired Meta Knight. | Its ZIP contains separate with/without dash-dance variants, requiring a manual choice. |

### Goofy Smash picks

| Mod | What it adds | CoffeeShop status |
| --- | --- | --- |
| [Kermit](https://gamebanana.com/mods/192512) | Kermit character swap. | Checked ZIP starts with `patch/` and `sound/`, so the game files need manual placement under `content/`. |
| [Fawful Has Fury](https://gamebanana.com/mods/192301) | Fawful character pack. | Checked ZIP starts with `Fawful_Pack/`. |
| [Waluigi (Wi-Fi Safe)](https://gamebanana.com/mods/191428) | Waluigi over Captain Falcon. | Checked ZIP contains costume-slot folders and separate UI art rather than root `content/`. |
| [Waluigi with moveset V1.5](https://gamebanana.com/mods/48472) | Waluigi with a distinct moveset. | Creator distributes a `.rar` and includes additional installation instructions. |
| [Shrek](https://gamebanana.com/mods/192238) | Shrek over Ganondorf with recolors and voice. | Creator distributes a `.rar`; the mod also needs the included slot instructions. |

These Smash projects may share fighter, parameter, UI or sound files. Build one tested setup at a time and follow the creator's region and game-version notes. We will promote a project into `game.json` only after a direct creator-authorized ZIP passes the [archive checks](CONTRIBUTING.md).
