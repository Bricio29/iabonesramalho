#!/usr/bin/env python3
# -*- coding: utf-8 -*-

with open('index.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Substituir aspas tipográficas por normais
replacements = [
    ('\u2018', "'"),  # ' para '
    ('\u2019', "'"),  # ' para '
    ('\u201C', '"'),  # " para "
    ('\u201D', '"'),  # " para "
]

for old, new in replacements:
    content = content.replace(old, new)

with open('index.js', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ Aspas tipográficas substituídas por aspas normais!')
print('✅ Total de substituições:', sum(content.count(old) for old, _ in replacements))
