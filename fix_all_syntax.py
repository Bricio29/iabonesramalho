#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re

with open('index.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Lista de template strings problemáticos que devem ser convertidos para aspas simples
fixes = [
    # Linha 925
    (
        r'await client\.sendMessage\(chatId, `Perfeito! Recebi sua logomarca! ✨\\n\\nNossa equipe vai analisar e se precisar de ajustes na arte, a gente te avisa! 👍`\);',
        "await client.sendMessage(chatId, 'Perfeito! Recebi sua logomarca! ✨\\n\\nNossa equipe vai analisar e se precisar de ajustes na arte, a gente te avisa! 👍');"
    ),
    # Linha 959 (se existir)
    (
        r'console\.log\(`✅ Cliente escolheu posição \$\{extraido\.posicaoModelo\} = \$\{codigoModelo\}`\);',
        "console.log('✅ Cliente escolheu posição ' + extraido.posicaoModelo + ' = ' + codigoModelo);"
    ),
]

for pattern, replacement in fixes:
    content = re.sub(pattern, replacement, content)

# Salvar
with open('index.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Correções aplicadas!")
