# Script for layout tokens on the page
# This program is distributed under the GNU General Public License v3.0
# Copyright (C) 2021 KizhiFox (https://github.com/KizhiFox/rpg-tokens-layout)

from pathlib import Path
from fpdf import FPDF

PADDING_TOP = 10
PADDING_LEFT = 25
VERTICAL_CELLS = 10
HORIZONTAL_CELLS = 6
CELL_SIZE = 27.7
MAX_PAGES = 10
PAGE_UNITS = 'mm'
PAGE_FORMAT = 'A4'
TOKENS_DIR = 'tokens'
TOKENS_LIST = 'tokens.txt'
OUTPUT_FILE = 'tokens.pdf'


pdf = FPDF(orientation='P', unit=PAGE_UNITS, format=PAGE_FORMAT)
total_lines = VERTICAL_CELLS * MAX_PAGES
grid = [[False] * HORIZONTAL_CELLS for i in range(total_lines)]  # grid[line][row]
tokens = []
with open(TOKENS_LIST, 'r', encoding='utf8') as f:
    for line in f.readlines():
        if line[0] == '#':
            continue
        line = line.strip()
        if line:
            raw = line.split('|')
            tokens.append({'filename': raw[0].strip(),
                           'size': int(raw[1].strip()),
                           'amount': int(raw[2].strip())})

pages = [[] for _ in range(MAX_PAGES)]
for token in tokens:
    for i in range(token['amount']):
        is_placed = False
        for v in range(total_lines):
            for h in range(HORIZONTAL_CELLS):
                # Check if it fits to the end of the page
                if v + token['size'] > total_lines or h + token['size'] > HORIZONTAL_CELLS or \
                        v % VERTICAL_CELLS + token['size'] > VERTICAL_CELLS:
                    continue
                # Check if cells are not being used
                is_space_free = True
                for token_v in range(v, v + token['size']):
                    for token_h in range(h, h + token['size']):
                        if grid[token_v][token_h]:
                            is_space_free = False
                if not is_space_free:
                    continue
                # Filling the grid
                for token_v in range(v, v + token['size']):
                    for token_h in range(h, h + token['size']):
                        grid[token_v][token_h] = True
                # Preparing the picture
                page_number = v // VERTICAL_CELLS
                pages[page_number].append(
                    {'filename': str(Path(TOKENS_DIR) / Path(token['filename'])),
                     'x': PADDING_LEFT + CELL_SIZE * h,
                     'y': PADDING_TOP + CELL_SIZE * (v % VERTICAL_CELLS),
                     'h': token['size'] * CELL_SIZE})
                is_placed = True
                break
            if is_placed:
                break

# Placement on a sheet
for images in filter(None, pages):
    pdf.add_page()
    for image in images:
        pdf.image(image['filename'], x=image['x'], y=image['y'], h=image['h'])
pdf.output(OUTPUT_FILE)
