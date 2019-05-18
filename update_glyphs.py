import os
import sys
import traceback
import urllib.request
import xml.etree.ElementTree
import json

REMOTE_GLYPHS_DATA_URL = 'https://material.io/tools/icons/static/data.json'
GLYPHS_DATA_PATH   = './glyphs_data.json'
GLYPHS_LIST_PATH   = './glyphs_list.txt'
GLYPH_PATH_PATTERN = './glyphs/%s/%s.svg'

# Register SVG namespace, so all SVG files will be saved correctly.
xml.etree.ElementTree.register_namespace('', 'http://www.w3.org/2000/svg')

def print_exception_info(info):
  exception_class, exception_text, exception_traceback = sys.exc_info()
  tb = traceback.format_tb(exception_traceback)
  tb = "Traceback:\n" + "".join(tb)
  print("Caught an exception (%s):\n  %s\nAdditional info:\n  %s\n%s" % (exception_class, exception_text, info, tb))

def download_file(url):
  response = urllib.request.urlopen(url)
  return response.read()

# Download an SVG glyph file, remove the background fill, and save it.
# If the background fill is not removed, the glyph will be a black square after importing it in FontForge.
def download_sanitized_svg(url, file_name):
  try:
    full_url = 'https://material.io/tools/icons/static/icons/' + url
    downloaded_data = download_file(full_url)
    root = xml.etree.ElementTree.fromstring(downloaded_data)
    for child in root:
      if 'fill' in child.attrib:
        root.remove(child)
    tree = xml.etree.ElementTree.ElementTree(root)
    tree.write(file_name)
  except Exception:
    print_exception_info("url: '%s', file_name: '%s'" % (url, file_name))

def update_glyphs_data():
  try:
    print("Reading local glyphs data.")
    with open(GLYPHS_DATA_PATH, 'r') as file:
      glyphs_data = json.load(file)
    glyphs_order = glyphs_data['order']
    glyphs_info  = glyphs_data['info']

    # Populate 'order' with missing glyph ids (ones that don't have 'info' entry).
    print("Searching for new glyphs.")
    no_glyph_added = True
    nonstandard_urls = {}
    downloaded_glyphs_data = json.loads(download_file(REMOTE_GLYPHS_DATA_URL))
    for category in downloaded_glyphs_data['categories']:
      for glyph in category['icons']:
        if not glyph['id'] in glyphs_info:
          glyphs_order.append(glyph['id'])
          print("Added new glyph '%s'." % glyph['id'])
          no_glyph_added = False
        if glyph.get('imageUrls'):
          nonstandard_urls[glyph['id']] = glyph['imageUrls']
    if no_glyph_added:
      print("No new glyphs found.")
      return

    # Fully update 'info' entries for all the glyph ids stored in 'order'.
    unicode_offset = 0xE000
    for glyph_index, glyph_id in enumerate(glyphs_order):
      glyphs_info[glyph_id] = {
        'urls': nonstandard_urls.get(glyph_id) or {
          'baseline': 'baseline-%s-24px.svg' % glyph_id,
          'outline':  'outline-%s-24px.svg'  % glyph_id,
          'round':    'round-%s-24px.svg'    % glyph_id,
          'twotone':  'twotone-%s-24px.svg'  % glyph_id,
          'sharp':    'sharp-%s-24px.svg'    % glyph_id,
        },
        'unicode_id': unicode_offset + glyph_index
      }

    # Save updated info to a file.
    with open(GLYPHS_DATA_PATH, 'w') as file:
      json.dump(glyphs_data, file)
    print("Updated local glyphs data.")
  except Exception:
    print_exception_info("REMOTE_GLYPHS_DATA_URL: '%s', GLYPHS_DATA_PATH: '%s'" % (REMOTE_GLYPHS_DATA_URL, GLYPHS_DATA_PATH))

def download_missing_glyphs():
  with open(GLYPHS_DATA_PATH, 'r') as file:
    glyphs_data = json.load(file)

  for glyph_id, glyphs_info in glyphs_data['info'].items():
    for glyph_type, glyph_url in glyphs_info['urls'].items():
      glyph_path = GLYPH_PATH_PATTERN % (glyph_type, glyph_id)
      if not os.path.isfile(glyph_path):
        print("Downloading '%s' [%s] ('%s') " % (glyph_id, glyph_type, glyph_url))
        download_sanitized_svg(glyph_url, glyph_path)

def update_glyphs_list():
  try:
    with open(GLYPHS_DATA_PATH, 'r') as file:
      glyphs_data = json.load(file)
    glyphs_order = glyphs_data['order']
    glyphs_info  = glyphs_data['info']

    with open(GLYPHS_LIST_PATH, 'w', encoding="utf-8") as file:
      for glyph_index, glyph_id in enumerate(glyphs_order):
        glyph_unicode_id = glyphs_info[glyph_id]['unicode_id']
        glyph_line = u'%s %s %s\n' % (hex(glyph_unicode_id)[2:], glyph_id, chr(glyph_unicode_id))
        file.write(glyph_line)
  except Exception:
    print_exception_info("GLYPHS_DATA_PATH: '%s', GLYPHS_LIST_PATH: '%s'" % (GLYPHS_DATA_PATH, GLYPHS_LIST_PATH))


# ====================================
#          SCRIPT EXECUTION
# ====================================

update_glyphs_data()
download_missing_glyphs()
update_glyphs_list()
