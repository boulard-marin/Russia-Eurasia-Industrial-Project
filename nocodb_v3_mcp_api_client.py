import requests
import json
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

NOCODB_MCP_URL = "https://app.nocodb.com/mcp/ncvlottre3sgvvvs"
NOCODB_TOKEN = "HeFPyX-Pwh9Tdpx3UDdHxJZ9bcTwNw-E"
BASE_ID = "p0ygj6vufqhhhsc"

TABLE_IDS = {
    "pipeline": "m0vdmxf9g5kdudb",
    "eiii": "muedfnxvjicb7vp",
    "master": "m70egqzk4zko1x9",
    "sector": "m7b71ocpsn32u1i",
    "whatif": "mgfkyltonzbmgj9"
}

HEADERS = {
    "xc-mcp-token": NOCODB_TOKEN,
    "Accept": "application/json, text/event-stream",
    "Content-Type": "application/json"
}

class NocoDBv3MCPClient:
    def __init__(self):
        self.url = NOCODB_MCP_URL
        self.headers = HEADERS
        self.base_id = BASE_ID
        self.table_ids = TABLE_IDS

    def _call(self, method, params=None, req_id=1):
        payload = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params or {},
            "id": req_id
        }
        try:
            r = requests.post(self.url, headers=self.headers, json=payload, timeout=20)
            lines = r.text.strip().split("\n")
            for line in lines:
                if line.startswith("data: "):
                    return json.loads(line[6:])
            return {"raw": r.text}
        except Exception as e:
            return {"error": str(e)}

    def count_records(self, table_key):
        tid = self.table_ids.get(table_key, table_key)
        res = self._call("tools/call", {"name": "countRecords", "arguments": {"tableId": tid}})
        text = res.get("result", {}).get("content", [{}])[0].get("text", "{}")
        try:
            return json.loads(text).get("count", 0)
        except:
            return text

    def query_records(self, table_key, page_size=5, page=1):
        tid = self.table_ids.get(table_key, table_key)
        res = self._call("tools/call", {
            "name": "queryRecords",
            "arguments": {
                "tableId": tid,
                "pageSize": page_size,
                "page": page
            }
        })
        text = res.get("result", {}).get("content", [{}])[0].get("text", "{}")
        try:
            return json.loads(text).get("records", [])
        except:
            return text

def main():
    print("==================================================")
    print(" 🛠️ NOCODB V3 MCP REMOTE API CONTROLLER CLIENT ")
    print(" Base: p0ygj6vufqhhhsc                            ")
    print("==================================================")

    client = NocoDBv3MCPClient()

    for key, tid in TABLE_IDS.items():
        count = client.count_records(key)
        records = client.query_records(key, page_size=1)
        print(f"\n[Table: {key.upper()}] ID: {tid}")
        print(f" -> Live Total Record Count: {count}")
        if isinstance(records, list) and records:
            sample_fields = list(records[0].get("fields", {}).keys())
            print(f" -> Field Schema ({len(sample_fields)} fields): {', '.join(sample_fields[:6])}...")
            print(f" -> Sample Record #1: {json.dumps(records[0].get('fields'), ensure_ascii=False)[:120]}...")

if __name__ == "__main__":
    main()
