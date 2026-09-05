#!/usr/bin/env bash
# Query the Content Calendar data source. Requires .env with NOTION_TOKEN and DATABASE_ID.
set -euo pipefail
cd "$(dirname "$0")"; set -a; source .env; set +a
# 1) Resolve the data source id from the database (API 2025-09-03: a database holds data_sources[])
DS=$(curl -s "https://api.notion.com/v1/databases/${DATABASE_ID}" \
  -H "Authorization: Bearer ${NOTION_TOKEN}" -H "Notion-Version: ${NOTION_VERSION:-2025-09-03}" \
  | python3 -c 'import sys,json; print(json.load(sys.stdin)["data_sources"][0]["id"])')
echo "data source: $DS"
# 2) Query it with the filter body
curl -s -X POST "https://api.notion.com/v1/data_sources/${DS}/query" \
  -H "Authorization: Bearer ${NOTION_TOKEN}" -H "Notion-Version: ${NOTION_VERSION:-2025-09-03}" \
  -H "Content-Type: application/json" --data @query-database.json \
  | python3 -c '
import sys, json
for r in json.load(sys.stdin)["results"]:
    p = r["properties"]
    name = "".join(t["plain_text"] for t in p["Name"]["title"])
    status = (p.get("Status", {}).get("status") or {}).get("name", "")
    print(f"{name:45s} {status}")'
