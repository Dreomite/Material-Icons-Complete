# Reference list:
# - FontForge Python API: https://fontforge.github.io/python.html
# - Glyph naming convention: http://www.typophile.com/node/10026
# - A little script example: https://stackoverflow.com/a/22135233

import sys
import json
import fontforge

GLYPH_DATABASE_PATH = './glyphs_data.json'
GLYPH_PATH_PATTERN = './glyphs/%s/%s.svg'
FONT_NAME_PATTERN = 'Material Icons Complete %s'
FONT_TYPES = {
  'Filled':   'baseline',
  'Outlined': 'outline',
  'Rounded':  'round',
  'Two-tone': 'twotone',
  'Sharp':    'sharp'
}
FONT_FORMATS = [
  'eot',
  'ttf',
  'otf',
  'svg',
  'woff',
  'woff2'
]
OUTPUT_DIR = './output/'

def initialize_font(glyph_database, font_type):
  font_name = FONT_NAME_PATTERN % font_type

  font = fontforge.font()
  font.familyname = font_name
  font.fullname   = font_name

  for glyph_id, glyph_info in glyph_database['info'].iteritems():
    print("Importing glyph [%s]: %s" % (font_type, glyph_id))
    unicode_id = glyph_info['unicode_id']
    unicode_name = 'uni' + hex(unicode_id).upper()[2:]
    char = font.createChar(unicode_id, unicode_name)
    char.importOutlines(GLYPH_PATH_PATTERN % (FONT_TYPES[font_type], glyph_id))
    char.width = 1000

  return font, font_name.replace(' ', '-')

def generate_fonts(font_types, font_formats):
  with open(GLYPH_DATABASE_PATH, 'r') as file:
    glyph_database = json.load(file)

  for font_type in font_types:
    font, font_name = initialize_font(glyph_database, font_type)

    for font_format in font_formats:
      output_file_name = OUTPUT_DIR + font_name + '.' + font_format
      print("Generating font file: %s" % output_file_name)
      font.generate(output_file_name)
      print("Done.")

# ====================================
#          SCRIPT EXECUTION
# ====================================

if len(sys.argv) > 3:
  sys.exit("Wrong number of arguments.")

if len(sys.argv) > 1:
  if not FONT_TYPES.get(sys.argv[1]):
    sys.exit("Specified font type does not exist.")
  font_types = [sys.argv[1]]
else:
  font_types = FONT_TYPES

if len(sys.argv) > 2:
  font_formats = [sys.argv[2]]
else:
  font_formats = FONT_FORMATS

generate_fonts(font_types, font_formats)
