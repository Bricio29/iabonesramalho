#!/usr/bin/env python3
# -*- coding: utf-8 -*-

with open('index.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Substituir a linha 925 (index 924) por uma versão correta
if len(lines) > 924:
    # Nova linha correta com template string
    new_line = "            await client.sendMessage(chatId, 'Perfeito! Recebi sua logomarca! ✨\\n\\nNossa equipe vai analisar e se precisar de ajustes na arte, a gente te avisa! 👍');\n"
    lines[924] = new_line
    print(f"✅ Linha 925 substituída")
    print(f"Antiga: {repr(lines[924][:80])}")
    print(f"Nova: {repr(new_line[:80])}")
else:
    print("❌ Arquivo muito pequeno")
    
with open('index.js', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("✅ Arquivo salvo!")
