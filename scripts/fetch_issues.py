import requests
import os
import pandas as pd


TOKEN = os.environ.get("GITHUB_TOKEN", "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")
OWNER = "LaNES288"
REPO = "DEMO"

headers = {
    "Authorization": f"token {TOKEN}"
}

url = f"https://api.github.com/repos/{OWNER}/{REPO}/issues?state=open&labels=status:backlog"

response = requests.get(url, headers=headers)
issues = response.json()

data = []

for issue in issues:
    data.append({
        "title": issue["title"],
        "created_at": issue["created_at"],
        "assignee": issue["assignee"]["login"] if issue["assignee"] else "Unassigned"
    })

df = pd.DataFrame(data)
df.to_csv("issues.csv", index=False)

print(f"Fetched {len(df)} backlog issues")
