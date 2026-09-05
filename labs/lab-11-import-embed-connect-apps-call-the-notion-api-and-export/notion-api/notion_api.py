#!/usr/bin/env python3
"""Minimal Notion API client for Lab 11 — query the Content Calendar, then create a page.

Usage:  python3 notion_api.py query
        python3 notion_api.py create
Reads NOTION_TOKEN, DATABASE_ID and NOTION_VERSION from .env in this folder (no extra packages).
"""
import json, os, sys, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
def load_env():
    env = {}
    for line in open(os.path.join(HERE, ".env")):
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1); env[k.strip()] = v.strip()
    return env
ENV = load_env()
API = "https://api.notion.com/v1"
HEADERS = {"Authorization": f"Bearer {ENV['NOTION_TOKEN']}",
           "Notion-Version": ENV.get("NOTION_VERSION", "2025-09-03"),
           "Content-Type": "application/json"}

def call(method, path, body=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(API + path, data=data, headers=HEADERS, method=method)
    with urllib.request.urlopen(req) as r:
        return json.load(r)

def data_source_id():
    db = call("GET", f"/databases/{ENV['DATABASE_ID']}")
    return db["data_sources"][0]["id"]          # a database holds one or more data sources

def query():
    ds = data_source_id()
    body = json.load(open(os.path.join(HERE, "query-database.json")))
    res = call("POST", f"/data_sources/{ds}/query", body)
    for row in res["results"]:
        p = row["properties"]
        name = "".join(t["plain_text"] for t in p["Name"]["title"])
        status = (p.get("Status", {}).get("status") or {}).get("name", "")
        print(f"{name:45s} {status}")
    print(f"{len(res['results'])} rows")

def create():
    ds = data_source_id()
    body = json.load(open(os.path.join(HERE, "create-page.json")))
    body["parent"] = {"data_source_id": ds}
    page = call("POST", "/pages", body)
    print("created:", page["url"])

if __name__ == "__main__":
    {"query": query, "create": create}.get(sys.argv[1] if len(sys.argv) > 1 else "", lambda: print(__doc__))()
