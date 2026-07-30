import os
import json
import urllib.request

# Notion API Integration Helper
NOTION_API_KEY = os.environ.get("NOTION_API_KEY", "your_integration_token_here")
NOTION_VERSION = "2022-06-8"

headers = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Content-Type": "application/json",
    "Notion-Version": NOTION_VERSION
}

print("Notion API Helper initialized.")
print("To import into Notion without API key: Use Notion's built-in 'Import > Markdown & CSV' and select the 'notion_workspace' folder.")
