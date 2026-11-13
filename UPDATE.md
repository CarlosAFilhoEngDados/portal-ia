# RADARNEXO — rotina de atualização diária

Objetivo: site pronto antes das 7h (America/Sao_Paulo), quando o Carlos chega.

## Arquivos
- `data/news.json`: notícias (`updated_at` + `items[]`). Campos por item:
  `id` (n001, n002… sequencial, nunca reutilizar), `title` (pt-BR), `date` (ISO `AAAA-MM-DD`, data de publicação da fonte),
  `category` (`claude` | `snowflake` | `microsoft` | `modelos` | `ferramentas` | `seguranca` | `dados` | `mundo`),
  `tags` (2–3 strings curtas), `summary` (1–2 frases em pt-BR), `source_name` (domínio), `url` (link real aberto na pesquisa),
  `priority` (`true` para claude/snowflake), `added` (data em que o item entrou no portal).
  Campos de impacto: `impact` (`alto` | `medio`) e `affects` (lista com `empresas` e/ou `pessoas`). **Obrigatórios** quando `category` = `mundo`;
  opcionais nas outras categorias (ex.: um zero-day de segurança pode levar `impact: "alto"`). O build.py falha se estiverem inválidos.

## Mundo Tech (aba `#/mundo`)
Tecnologia em geral com grande impacto em organizações e pessoas, mesmo sem relação direta com IA. Entra:
- **Quedas/indisponibilidades grandes** de serviços usados por muitas empresas (Microsoft 365/Exchange/Teams, Google Workspace, AWS/Azure/GCP, Cloudflare, bancos/Pix, operadoras).
- **Vazamentos e invasões grandes**, principalmente envolvendo **acesso, identidade e credenciais** (senhas, tokens, MFA, SSO, Entra ID/Okta, fornecedores/MSPs com acesso aos clientes).
- **Vulnerabilidades críticas exploradas** (CISA KEV, zero-days, bypass de autenticação) em produtos de uso corporativo amplo.
- **Incidentes de nuvem/SaaS** com relatório de causa (post-mortem) relevante para resiliência.
- **Regulação e eventos do setor** com efeito prático (marco da IA/PL 2338, ANPD/LGPD, AI Act, decisões judiciais).
Não entra: rumores, notas sem fonte primária ou reportagem confiável, incidentes pequenos/locais.
**Impacto `alto`** = queda ampla em andamento ou recém-encerrada, ou falha crítica de acesso/credencial explorada ativamente. Vai sozinho para a faixa
"Alto impacto" da home (até 4 itens `impact: "alto"` dos últimos 14 dias, de qualquer categoria). **`medio`** = relevante, mas restrito a um setor/país ou já resolvido.
Datas e números da reportagem devem ser conferidos na página; para incidentes em andamento, dizer o status na hora da coleta (ex.: "recuperação gradual em 13/11").
- `data/site.json`: `highlights` (ids dos destaques: o 1º vira o card grande "Destaque" de Últimas Notícias, o 2º–4º vão em "Destaques da Semana"; o 5º não aparece na home), `iguatemi` (sugestões [título, texto]),
  `dates` (timeline [iso, rótulo, o quê, fornecedor]), `trainings` (candidatos [categoria, título, descrição]; sempre "aguardando aprovação").
- `template.html`: layout RADARNEXO (CSS/JS e imagens base64 inline; rotas por hash #/noticias, #/mundo[/alto|medio|todos[/empresas|pessoas]], #/post/<id>, #/busca/<termo>, #/iguatemi, #/agenda, #/treinamentos, #/sobre). Não editar dados no template. `build.py`: valida o JSON e gera `index.html` autocontido (abre do disco).

## Passo a passo (diário, ~6h)
1. **Pesquisar** novidades publicadas desde o último `updated_at` em news.json (WebSearch/WebFetch), por categoria:
   Claude/Anthropic (anthropic.com/news, claude.com, changelog do Claude Code), Snowflake (snowflake.com/en/blog, docs.snowflake.com/release-notes),
   Microsoft (blog do Copilot Studio, learn.microsoft.com Cowork what's new, Message Center, techcommunity), modelos de todos os labs,
   ferramentas (GitHub, Cursor, OpenAI, MCP), segurança (Patch Tuesday, advisories de MCP/agentes, NVD/GHSA), dados (Databricks, Fabric/OneLake, Iceberg, vetores),
   Mundo Tech (status/health das grandes nuvens e SaaS, CISA KEV, AP/Reuters/BBC/CIO/The Register/Ars/BleepingComputer, Valor/Convergência Digital para regulação BR).
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
   Conferir visualmente (hero RADARNEXO, faixa "Alto impacto" quando houver item alto nos últimos 14 dias, Últimas Notícias + Destaques da Semana, faixa "Atualizado em", categorias com contagem, nada estourando o layout). Os 3 primeiros itens de iguatemi/trainings/dates aparecem na home; o resto nas páginas próprias. "Prioridades" = itens priority=true mais recentes fora dos destaques.
8. **Publicar/avisar**: se houver hospedagem configurada, publicar `index.html`; avisar o Carlos com 3–4 manchetes do dia + link.
