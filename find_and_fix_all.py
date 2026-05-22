#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import subprocess
import re

# Ler o arquivo
with open('index.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Encontrar todos os erros de sintaxe
errors_found = []
while True:
    result = subprocess.run(['node', '-c', 'index.js'], capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ Nenhum erro de sintaxe encontrado!")
        break
    
    # Extrair número da linha do erro
    error_output = result.stderr
    match = re.search(r'/index.js:(\d+)', error_output)
    
    if match:
        line_num = int(match.group(1))
        print(f"🔍 Erro encontrado na linha {line_num}")
        
        if line_num in errors_found:
            print(f"❌ Erro já processado anteriormente na linha {line_num}. Parando.")
            break
        
        errors_found.append(line_num)
        
        # Corrigir a linha substituindo template string por concatenação
        if line_num <= len(lines):
            old_line = lines[line_num - 1]
            print(f"   Antiga: {old_line[:80]}")
            
            # Converter template strings para concatenação de strings simples
            new_line = old_line
            
            # Padrão 1: `texto ${variavel} mais texto`
            def replace_template(match):
                content = match.group(1)
                # Substituir ${...} por ' + ... + '
                content = re.sub(r'\$\{([^}]+)\}', r"' + \1 + '", content)
                # Limpar concatenações vazias
                content = content.replace(" + '' + ", " + ")
                content = content.replace("'' + ", "")
                content = content.replace(" + ''", "")
                return "'" + content + "'"
            
            new_line = re.sub(r'`([^`]*)`', replace_template, new_line)
            
            lines[line_num - 1] = new_line
            print(f"   Nova:   {new_line[:80]}")
            
            # Salvar
            with open('index.js', 'w', encoding='utf-8') as f:
                f.writelines(lines)
            print(f"✅ Linha {line_num} corrigida. Verificando novamente...")
        else:
            print(f"❌ Número de linha {line_num} fora do alcance")
            break
    else:
        print("❌ Não foi possível extrair o número da linha do erro")
        print(error_output[:200])
        break
    
    if len(errors_found) > 50:
        print("❌ Muitos erros encontrados. Parando.")
        break

print(f"\n📊 Total de linhas corrigidas: {len(errors_found)}")
