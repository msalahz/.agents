---
name: favicon-generator
description: Generate favicon.ico, favicon PNGs, Android and Apple touch icons, and site.webmanifest from a single-color brand logo, and save the generator config in the repo. Use when the user asks for a favicon, app icons, or a web manifest from a logo image.
metadata:
  author: "Mohammed Zaghloul <m.salahz86@gmail.com>"
  version: "0.1.0"
---

# Favicon generator

The skill folder holds a self-contained package under `scripts/`: `generate-favicons.ts`, its `package.json`, and `favicons.config.example.json`. The script reads one JSON config, recolors the logo's alpha channel, and writes every icon plus the manifest into the repo's public directory. The source logo must be a single-color glyph on a transparent background; only its alpha channel is used, so the glyph's own color does not matter.

## 1. Collect the inputs

Required: the logo path and the repo's public directory. Ask for the glyph color as a hex value; if the user gives a screenshot of an icon to match, sample its stroke color with sharp and confirm the hex. Ask for the manifest `name`, `short_name`, `theme_color`, and `background_color` every time; do not fill them from `package.json`. Defaults the user can override: transparent glyph coverage `1`, touch icon coverage `0.7`, touch icon white glyph on a `#1f1f1f` tile, display `standalone`. At most three questions per round.

Done when: every config field has a value the user supplied or accepted.

## 2. Write the config into the repo

Copy `favicons.config.example.json` to `<repo>/scripts/favicons.config.json` and fill it with the collected values. `source` and `outputDir` are relative to the config file, so write them as `../public/logo.png` and `../public`.

Done when: the config file exists in the repo and parses as JSON.

## 3. Generate

Install the script's dependencies once with `pnpm install --dir <skill>/scripts`, then run:

```sh
pnpm --dir <skill>/scripts generate <repo>/scripts/favicons.config.json
```

The script prints each written file and the head link block.

Done when: `favicon.ico`, `favicon-16x16.png`, `favicon-32x32.png`, `android-chrome-192x192.png`, `android-chrome-512x512.png`, `apple-touch-icon.png`, and `site.webmanifest` exist in the public directory.

## 4. Verify

Upscale `favicon-32x32.png` with nearest-neighbour to about 192px onto a white tile and a dark tile, view the result, and confirm the glyph is centred, unclipped, and legible on both.

Done when: the preview has been viewed and any clipping or contrast problem has been fixed by adjusting the config and rerunning step 3.

## 5. Report

Do not edit the app head. Report the files written, the config path, the printed head link block for the user to paste, and this regeneration command:

```sh
pnpm --dir <skill>/scripts generate scripts/favicons.config.json
```

Done when: the report lists every written file, the config path, the link block, and the regeneration command.
