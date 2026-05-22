#!/usr/bin/env python3
# -*- coding: utf-8 -*-

with open('index.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Substituir template strings problemáticos por concatenação
replacements = {
    925: "            await client.sendMessage(chatId, 'Perfeito! Recebi sua logomarca! ✨\\n\\nNossa equipe vai analisar e se precisar de ajustes na arte, a gente te avisa! 👍');\n",
    959: "                console.log('✅ Cliente escolheu posição ' + extraido.posicaoModelo + ' = ' + codigoModelo);\n",
    973: "            console.log('📸 Cliente informou objetivo: ' + extraido.usoEvento + ' - Preparando para enviar modelos');\n",
}

for line_num, new_content in replacements.items():
    if len(lines) >= line_num:
        lines[line_num - 1] = new_content
        print(f"✅ Linha {line_num} corrigida")

with open('index.js', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("✅ Todas as correções aplicadas!")
