#!/usr/bin/env python3
"""Lê data/news.json + data/site.json e gera index.html autocontido (abre direto do disco)."""
import json, pathlib, datetime, sys
from zoneinfo import ZoneInfo
ROOT = pathlib.Path(__file__).resolve().parent
news = json.loads((ROOT/"data/news.json").read_text(encoding="utf-8"))
if "--touch" in sys.argv:
    news["updated_at"] = datetime.datetime.now(ZoneInfo("America/Sao_Paulo")).replace(microsecond=0).isoformat()
    (ROOT/"data/news.json").write_text(json.dumps(news, ensure_ascii=False, indent=2), encoding="utf-8")
site = json.loads((ROOT/"data/site.json").read_text(encoding="utf-8"))
# validação mínima
req = {"id","title","date","category","tags","summary","source_name","url","priority"}
cats = {"claude","snowflake","microsoft","modelos","ferramentas","seguranca","dados"}
ids=set()
for it in news["items"]:
    miss = req - it.keys()
    assert not miss, f"{it.get('id')}: faltando {miss}"
    assert it["category"] in cats, f"{it['id']}: categoria inválida"
    assert it["url"].startswith("http"), f"{it['id']}: url inválida"
    datetime.date.fromisoformat(it["date"])
    assert it["id"] not in ids, f"id duplicado {it['id']}"; ids.add(it["id"])
site["highlights"] = [h for h in site.get("highlights", []) if h in ids]
payload = json.dumps({"news": news, "site": site}, ensure_ascii=False).replace("</", "<\\/")
tpl = (ROOT/"template.html").read_text(encoding="utf-8")
(ROOT/"index.html").write_text(tpl.replace("/*__DATA__*/", payload), encoding="utf-8")
print(f"index.html gerado: {len(news['items'])} itens, destaques={len(site['highlights'])}, updated_at={news['updated_at']}")
