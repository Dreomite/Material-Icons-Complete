This project is a bunch of python scripts for downloading all the glyphs from material icons site and generating fonts with them.

Resulting fonts are not compatible with original fonts as they have different Unicode indices. However, they will always be backward-compatible with themselves in case of material icons update.

Just a little reminder that fonts do not support semi-transparency. It's either fully opaque, or fully transparent. All the fancy semi-transparent indicators will look like this (Note battery and wi-fi indicators):

![image](https://user-images.githubusercontent.com/35058624/51192850-8727cf80-18f8-11e9-8db5-7bb20b503732.png)


# Project structure

`./glyphs_list.txt` - Contains glyph Unicode IDs, their names and Unicode characters themselves for easy copying.

`./glyphs_data.json` - All the data needed for preserving right glyph order, their download location, type, Unicode indices, etc.

`./glyphs/` - Downloaded sanitized SVG glyphs of 5 different types ready to be converted to different fonts.

All the python scripts are described separately.

# `update_glyphs.py`

Requires Python 3 to run.

* Parses glyphs data from material.io .
* If new glyph detected, adds it to `glyphs_data.json` preserving the order of already existing glyphs so updated font will be compatible with previously generated ones.
* Downloads missing glyph SVGs and sanitizes them, so they could be used for font creating.
* Updates `glyphs_list.txt`

If you want it to parse everything as in the first time and redownload all the glyphs

1. Delete all SVGs inside `/glyphs/*/`
2. Replace `glyphs_data.json` contents with
   ```
   {"order": [], "info": {}}
   ```

### How to use

`python ./update_glyphs.py`

# `generate_font.py`

Requires [FontForge](https://github.com/fontforge/fontforge/releases) which is bundled with its own Python 2.7 distribution.

- Generates font based on selected type and format

Allowed font types:

- `Filled`
- `Outlined`
- `Rounded`
- `Two-tone`
- `Sharp`

Allowed font formats:

- `eot`
- `ttf`
- `otf`
- `svg`
- `woff`
- `woff2`

(Actually, any format supported by FontForge. These are just default ones.)

### How to use

Instruction for Windows users:
1. Run "FontForge interactive console"
2. Move to the root project directory
3. `fontforge -script generate_font.py [FONT_TYPE [FONT_FORMAT]]`

If `FONT_FORMAT` is not set, all 6 font formats are generated.
If `FONT_TYPE` is not set, all 6 font formats are generated for all 5 font types.

**!!IMPORTANT!!**: There's a bug in font forge I could not get around. If you'll try to create `otf` or `woff` files for `Outlined` font type, FontForge will hang. It is caused by `call_end` and `movie_creation` glyphs. I don't know how to solve it.
