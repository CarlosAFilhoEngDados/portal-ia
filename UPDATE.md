# Portal IA · Carlos — rotina de atualização diária

Objetivo: site pronto antes das 7h (America/Sao_Paulo), quando o Carlos chega.

## Arquivos
- `data/news.json`: notícias (`updated_at` + `items[]`). Campos por item:
  `id` (n001, n002… sequencial, nunca reutilizar), `title` (pt-BR), `date` (ISO `AAAA-MM-DD`, data de publicação da fonte),
  `category` (`claude` | `snowflake` | `microsoft` | `modelos` | `ferramentas` | `seguranca` | `dados`),
  `tags` (2–3 strings curtas), `summary` (1–2 frases em pt-BR), `source_name` (domínio), `url` (link real aberto na pesquisa),
  `priority` (`true` para claude/snowflake), `added` (data em que o item entrou no portal).
- `data/site.json`: `highlights` (ids dos 5 destaques do dia, o 1º vira o card grande), `iguatemi` (sugestões [título, texto]),
  `dates` (timeline [iso, rótulo, o quê, fornecedor]), `trainings` (candidatos [categoria, título, descrição]; sempre "aguardando aprovação").
- `template.html`: layout (CSS/JS inline). `build.py`: valida o JSON e gera `index.html` autocontido (abre do disco).

## Passo a passo (diário, ~6h)
1. **Pesquisar** novidades publicadas desde o último `updated_at` em news.json (WebSearch/WebFetch), por categoria:
   Claude/Anthropic (anthropic.com/news, claude.com, changelog do Claude Code), Snowflake (snowflake.com/en/blog, docs.snowflake.com/release-notes),
   Microsoft (blog do Copilot Studio, learn.microsoft.com Cowork what's new, Message Center, techcommunity), modelos de todos os labs,
   ferramentas (GitHub, Cursor, OpenAI, MCP), segurança (Patch Tuesday, advisories de MCP/agentes, NVD/GHSA), dados (Databricks, Fabric/OneLake, Iceberg, vetores).
2. **Verificar** cada item: abrir a página da fonte, confirmar data e fatos. Nunca inventar item, data ou link; descartar o que não confirmar.
   Evitar duplicatas (mesma URL ou mesmo anúncio já presente).
3. **Adicionar** ao `items` de news.json com o próximo `id` livre e `added` = hoje.
4. **Podar**: remover itens com `date` mais antigo que 30 dias antes de hoje (exceto se ainda estiver em `highlights`).
5. **Atualizar site.json**: escolher 5 `highlights` (priorizar Claude e Snowflake, depois segurança crítica); remover datas já passadas
   de `dates` e incluir novos prazos; revisar `iguatemi` e `trainings` se surgir algo relevante (treinamentos continuam só como sugestão;
   não criar nenhum sem aprovação do Carlos).
6. **Gerar**: `python3 build.py --touch` (atualiza `updated_at` para agora em America/Sao_Paulo e escreve index.html). O script falha se faltar campo, categoria inválida, URL inválida ou id duplicado.
7. **Screenshot**: com o servidor local no ar (`python3 -m http.server 8765 --directory /workspace/portal-ia &`):
   ```
   google-chrome --headless=new --no-sandbox --disable-gpu --hide-scrollbars --window-size=1440,2600 \
     --virtual-time-budget=4000 --screenshot=/workspace/portal-ia/screenshot.png http://localhost:8765/index.html
   google-chrome --headless=new --no-sandbox --disable-gpu --hide-scrollbars --window-size=390,2400 \
     --virtual-time-budget=4000 --screenshot=/workspace/portal-ia/screenshot-mobile.png http://localhost:8765/index.html
   ```
   Conferir visualmente (hero com 5 cards, chips, nada estourando o layout).
8. **Publicar/avisar**: se houver hospedagem configurada, publicar `index.html`; avisar o Carlos com 3–4 manchetes do dia + link.
