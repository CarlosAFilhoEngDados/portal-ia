# RadarNexo

RadarNexo é o portal estático de notícias de IA, dados e tecnologia, em português. A página reúne destaques do dia, filtros por categoria (Claude, Snowflake, Microsoft, modelos, ferramentas, segurança e dados), prazos, sugestões para o Iguatemi e treinamentos ainda aguardando aprovação. Tudo cabe em um único `index.html` autocontido, gerado a partir de `data/news.json`, `data/site.json` e `template.html`.

Site: https://carlosafilhoengdados.github.io/portal-ia/

## Como reconstruir

Na raiz do repositório:

```bash
python3 build.py --touch
```

O comando grava `updated_at` em `data/news.json` com o horário atual em `America/Sao_Paulo`, valida ids, categorias, datas e URLs, e reescreve `index.html`. Sem `--touch`, o script só regenera a página e mantém a data de atualização.

A rotina diária de pesquisa, poda e publicação está em [UPDATE.md](UPDATE.md).

## Publicação

Cada push na branch `main` dispara [`.github/workflows/pages.yml`](.github/workflows/pages.yml). O workflow publica a raiz do repositório no GitHub Pages (fonte: GitHub Actions). O arquivo `.nojekyll` impede o processamento pelo Jekyll.
