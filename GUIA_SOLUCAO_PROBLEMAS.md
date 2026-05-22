# Guia de Solução de Problemas - Bot Bonés Ramalho

## ✅ Problema: Bot fica tentando conectar mas não consegue

### Causa
Múltiplas instâncias do Chrome/Puppeteer rodando simultaneamente, causando conflito de acesso à pasta `.wwebjs_auth/session`.

### Solução Aplicada

1. **Script `start.sh` melhorado** para matar todos os processos antes de iniciar:
   - Mata processos Node.js
   - Mata TODAS as instâncias do Chrome/Chromium (incluindo "Google Chrome for Testing")
   - Remove arquivos de lock (SingletonLock, SingletonCookie, SingletonSocket)
   - Aguarda 3 segundos para garantir limpeza completa

2. **Configuração do Puppeteer simplificada**:
   - Removidas flags problemáticas (`--single-process`, `--no-zygote`)
   - Mantidas apenas flags essenciais para funcionar headless
   - Timeout aumentado para 60 segundos

### Como Usar Agora

```bash
# Sempre use npm start (nunca node index.js diretamente)
npm start

# O script automaticamente:
# 1. Limpa processos anteriores
# 2. Remove locks
# 3. Inicia o bot
```

## 🔧 Comandos Úteis

### Se o bot travar ou não conectar

```bash
# 1. Parar TUDO
pkill -9 -f "Google Chrome for Testing"
pkill -9 node

# 2. Limpar locks
cd /caminho/do/projeto
rm -f .wwebjs_auth/session/Singleton*

# 3. Aguardar 3 segundos e tentar novamente
sleep 3 && npm start
```

### Verificar processos rodando

```bash
# Ver quantos Chrome/Node estão rodando
ps aux | grep -E "(chrome|node)" | grep -v grep

# Se aparecer mais de 10-15 processos, há problema
```

### Resetar completamente (perder sessão)

```bash
# Apenas se REALMENTE necessário
pkill -9 node
pkill -9 -f "chrome"
rm -rf .wwebjs_auth .wwebjs_cache
npm start
# Vai pedir QR Code novamente
```

## 📊 Comportamento Esperado

### Inicialização Normal

```
🧹 Limpando processos residuais...
✅ Limpeza concluída!
🚀 Iniciando Bot Bonés Ramalho...
⚙️ Configurando cliente WhatsApp...
✅ Cliente configurado!
🚀 Bot Bonés Ramalho iniciado!
🔄 Inicializando conexão com WhatsApp...
📡 Tentativa 1 de 3...
📱 Escaneie o QR Code abaixo com seu WhatsApp:
[QR CODE APARECE]
✅ Conexão estabelecida com sucesso!
✅ Bot conectado ao WhatsApp!
🏢 Sistema Bonés Ramalho ativo!
```

### O que significa cada mensagem

- `📡 Tentativa X de 3...` - Normal, bot tenta até 3 vezes se houver erro temporário
- `✅ Conexão estabelecida com sucesso!` - Puppeteer/Chrome iniciou corretamente
- `✅ Bot conectado ao WhatsApp!` - Autenticação concluída (QR Code escaneado ou sessão restaurada)
- `🔐 Autenticação realizada com sucesso!` - Sessão anterior foi restaurada (sem QR Code)

## ⚠️ Sinais de Problema

### Bot travado

**Sintoma:** Fica em "📡 Tentativa 1 de 3..." por mais de 60 segundos sem mostrar QR Code ou erro

**Solução:**
```bash
# Ctrl+C para parar
# Rodar limpeza completa
pkill -9 node && pkill -9 -f "chrome"
sleep 3
npm start
```

### Múltiplos processos Chrome

**Sintoma:** `ps aux | grep chrome` mostra várias instâncias antigas (com horas de tempo de execução)

**Solução:**
```bash
pkill -9 -f "Google Chrome for Testing"
pkill -9 -f "chrome_crashpad"
sleep 2
npm start
```

### Erro "The browser is already running"

**Sintoma:** Mensagem de erro dizendo que o browser já está rodando

**Solução:**
```bash
rm -f .wwebjs_auth/session/Singleton*
pkill -9 -f "chrome"
npm start
```

## 🔐 Persistência de Sessão

### Como funciona

- **Primeira vez:** Escaneia QR Code → Sessão salva em `.wwebjs_auth/`
- **Próximas vezes:** Conecta automaticamente sem QR Code
- **Se der erro:** Sistema tenta 3 vezes antes de falhar

### Quando a sessão expira

- Depois de ~2 semanas sem usar
- Se o WhatsApp detectar atividade suspeita
- Se você desconectar manualmente no celular

**Solução:** Apenas escaneie o QR Code novamente

## 📸 Envio de Imagens

### Comportamento esperado

1. Cliente informa objetivo (ex: "Seria para brinde, equipe de atletismo")
2. Bot detecta automaticamente
3. Bot envia mensagem: "Perfeito! Vou te mostrar os modelos ideais..."
4. Bot envia 3 fotos de modelos recomendados
5. Cada foto com legenda completa (nome, código, descrição, preços)

### Logs de debug

Durante o envio, você verá:
```
📸 Cliente informou objetivo: brinde, equipe de atletismo
📸 Enviando 3 modelos recomendados para 5584999999999@c.us
🔍 Verificando arquivo: ./assets/modelos/BRBSP10.jpeg
✅ Arquivo encontrado! Preparando para enviar...
📤 Enviando imagem para 5584999999999@c.us...
✅ Imagem enviada com sucesso!
```

### Se as imagens não forem enviadas

1. Verifique se a pasta `assets/modelos/` existe e contém as imagens
2. Verifique os logs para identificar qual arquivo não foi encontrado
3. Confirme que o cliente realmente informou o objetivo de uso

## 💡 Dicas Importantes

1. **SEMPRE use `npm start`** - Nunca `node index.js` diretamente
2. **Aguarde o QR Code** aparecer antes de escanear
3. **Mantenha o terminal aberto** enquanto o bot estiver rodando
4. **Monitore os logs** para identificar problemas rapidamente
5. **Não rode múltiplas instâncias** ao mesmo tempo

## 📞 Suporte

Se o problema persistir:

1. Capture os logs completos do terminal
2. Execute `ps aux | grep -E "(chrome|node)" | grep -v grep` e capture o resultado
3. Verifique se há erros específicos no final do log
4. Tente resetar completamente removendo `.wwebjs_auth`
