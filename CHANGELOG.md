# Changelog - Bot Bonés Ramalho

## [Correções 10/02/2026]

### 🔍 Busca por Keywords em Modelos e Estilos

**Problema:** Quando o cliente pedia para ver modelos por características (ex: "foto de aba reta"), o sistema não enviava a imagem.

**Soluções aplicadas:**
1. ✅ Criada função `buscarPorKeywords()` que busca em todas as keywords do catálogo
2. ✅ Integrada busca inteligente no fluxo de processamento de mensagens
3. ✅ Detecta contexto: diferencia pedido para ver vs. escolha
4. ✅ Adicionados logs detalhados para facilitar debug

**Comportamento esperado:**
- Cliente: "Você conseguiria mandar foto de um modelo de aba reta?"
- Sistema busca "aba reta" nas keywords
- Encontra modelo BRART06
- Envia foto + legenda completa

**Keywords disponíveis:**
- Modelos: "aba reta", "trucker", "dad hat", "americano", "6 gomos", etc.
- Estilos: "silk 3d", "bordado", "emborrachado", "alto relevo"

---

### 🔄 Correção de Fluxo Duplicado e Repetições

**Problema 1:** IA repetindo a pergunta do cliente antes de responder.
- Cliente: "Como funciona os bonés personalizados?"
- Bot: "Como funciona os bonés personalizados?" (repetindo)
- Bot: [resposta correta]

**Problema 2:** Fluxo duplicado ao enviar modelo específico via keywords.
- Bot enviava foto + pergunta "O que achou?"
- Logo depois enviava outra mensagem genérica (duplicação)

**Soluções aplicadas:**
1. ✅ Adicionada regra explícita no prompt da IA para NUNCA repetir a pergunta do cliente
2. ✅ Implementada flag `perguntaEspecificaEnviada` no objeto extraido
3. ✅ Sistema detecta quando pergunta específica foi enviada e pula geração de resposta adicional
4. ✅ Adicionado log: "Pergunta específica já foi enviada, pulando geração de resposta da IA"

**Comportamento esperado:**
- Cliente: "Foto de modelo de aba reta?"
- Bot: [Envia foto do BRART06]
- Bot: "O que achou do Aba Reta? Se quiser ver mais detalhes..."
- [FIM - sem mensagem adicional]

**Arquivos modificados:**
- `index.js` (linhas 978, 1138, 1498-1508)

---

## [Correções 09/02/2026]

### 🖼️ Envio de Imagens Corrigido

**Problema:** O bot não estava enviando fotos dos modelos quando o cliente informava o objetivo.

**Soluções aplicadas:**
1. ✅ Modificado o prompt da IA para **OBRIGATORIAMENTE** marcar `querVerModelos: true` quando o cliente informar o objetivo de uso
2. ✅ Adicionada lógica de **forçar envio de imagens** quando `usoEvento` for detectado
3. ✅ Implementado flag `jaViuModelos` para evitar envio duplicado
4. ✅ Adicionados **logs detalhados** em cada etapa do envio de imagens
5. ✅ Implementado fallback para caminho absoluto caso caminho relativo falhe
6. ✅ Mensagem introdutória clara antes do envio das fotos

**Comportamento esperado:**
- Cliente informa objetivo (ex: "Seria para brinde, equipe de atletismo")
- Sistema detecta `usoEvento: "brinde, equipe de atletismo"`
- Sistema marca automaticamente `querVerModelos: true`
- Bot envia mensagem: "Perfeito! Vou te mostrar os modelos ideais para o que você precisa! 🧢✨"
- Bot envia 3 fotos de modelos recomendados com legendas completas

### 🔐 Persistência de Sessão do WhatsApp

**Problema:** Bot precisava escanear QR Code toda vez que era reiniciado.

**Soluções aplicadas:**
1. ✅ Modificado sistema de retry para **NÃO LIMPAR** a pasta `.wwebjs_auth`
2. ✅ Apenas limpa `.wwebjs_cache` (cache temporário) em caso de erro
3. ✅ Removido `.wwebjs_auth` do `.gitignore` (comentado com instrução)
4. ✅ Adicionado parâmetro `restartOnAuthFail: true` no cliente
5. ✅ Configurado `webVersionCache` para usar versão estável do WhatsApp Web

**Comportamento esperado:**
- Primeira conexão: Escanear QR Code normalmente
- Próximas conexões: Conecta automaticamente sem precisar de QR Code
- A sessão fica salva em `.wwebjs_auth/`

### 🛠️ Melhorias de Estabilidade

1. ✅ Timeout aumentado de 30s para 60s
2. ✅ Handler `remote_session_saved` adicionado
3. ✅ Logs muito mais detalhados para debug
4. ✅ Tratamento de erro melhorado (não encerra processo prematuramente)

### 📝 Instruções de Uso

**Para conectar pela primeira vez:**
```bash
npm start
# Escaneie o QR Code
# A sessão será salva automaticamente
```

**Para reconectar (sem QR Code):**
```bash
npm start
# Conectará automaticamente!
```

**Se precisar reconectar do zero:**
```bash
rm -rf .wwebjs_auth .wwebjs_cache
npm start
# Escaneie o QR Code novamente
```

### 🧪 Como Testar o Envio de Imagens

1. Envie mensagem inicial (ex: "Olá")
2. Informe seu nome quando solicitado
3. **Informe o objetivo** (ex: "Seria para brinde, equipe de atletismo")
4. ✅ O bot deve **automaticamente**:
   - Enviar mensagem introdutória
   - Enviar 3 fotos de modelos recomendados
   - Cada foto com legenda completa (nome, código, descrição, preços)

### 📊 Logs para Monitoramento

Agora o sistema exibe logs detalhados:
- `📸 Cliente informou objetivo: ... - Preparando para enviar modelos`
- `📸 Enviando X modelos recomendados para ...`
- `🔍 Verificando arquivo: ...`
- `✅ Arquivo encontrado! Preparando para enviar...`
- `📤 Enviando imagem para ...`
- `✅ Imagem enviada com sucesso!`
- `✅ Todas as fotos foram enviadas para ...`

Se aparecer erro, os logs mostrarão exatamente onde falhou.
