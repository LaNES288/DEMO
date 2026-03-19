import pandas as pd
from datetime import datetime, timezone
import json

# Load data
df = pd.read_csv("issues.csv")

# Convert datetime
df["created_at"] = pd.to_datetime(df["created_at"], utc=True)
now = datetime.now(timezone.utc)

# Metrics
df["age_days"] = (now - df["created_at"]).dt.days

total_issues = len(df)
avg_age = round(df["age_days"].mean(), 1) if total_issues > 0 else 0

oldest = df.sort_values("age_days", ascending=False).head(5)
assignees = df["assignee"].value_counts()

# Prepare chart data
assignee_labels = list(assignees.index)
assignee_values = list(assignees.values)

# Age buckets
bins = [0, 7, 30, 90, 9999]
labels = ["0-7 days", "8-30 days", "31-90 days", "90+ days"]
df["age_bucket"] = pd.cut(df["age_days"], bins=bins, labels=labels)

age_dist = df["age_bucket"].value_counts().sort_index()

age_labels = list(age_dist.index.astype(str))
age_values = list(age_dist.values)

# HTML Dashboard
html = f"""
<html>
<head>
    <title>Backlog Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {{
            font-family: Arial;
            background-color: #f4f6f8;
            margin: 20px;
        }}
        .container {{
            max-width: 1200px;
            margin: auto;
        }}
        .cards {{
            display: flex;
            gap: 20px;
        }}
        .card {{
            flex: 1;
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0px 2px 5px rgba(0,0,0,0.1);
        }}
        h1 {{
            margin-bottom: 10px;
        }}
        .charts {{
            display: flex;
            gap: 20px;
            margin-top: 20px;
        }}
        canvas {{
            background: white;
            padding: 10px;
            border-radius: 10px;
        }}
    </style>
</head>

<body>
<div class="container">

<h1>📊 Backlog Dashboard</h1>

<div class="cards">
    <div class="card">
        <h3>Total Issues</h3>
        <h1>{total_issues}</h1>
    </div>
    <div class="card">
        <h3>Average Age</h3>
        <h1>{avg_age} days</h1>
    </div>
</div>

<div class="charts">
    <canvas id="assigneeChart"></canvas>
    <canvas id="ageChart"></canvas>
</div>

<h2>⏳ Oldest Issues</h2>
{oldest.to_html(index=False)}

</div>

<script>
const assigneeChart = new Chart(document.getElementById('assigneeChart'), {{
    type: 'bar',
    data: {{
        labels: {json.dumps(assignee_labels)},
        datasets: [{{
            label: 'Issues per Assignee',
            data: {json.dumps(assignee_values)}
        }}]
    }}
}});

const ageChart = new Chart(document.getElementById('ageChart'), {{
    type: 'pie',
    data: {{
        labels: {json.dumps(age_labels)},
        datasets: [{{
            label: 'Age Distribution',
            data: {json.dumps(age_values)}
        }}]
    }}
}});
</script>

</body>
</html>
"""

# Save dashboard
with open("docs/index.html", "w") as f:
    f.write(html)

print("Professional dashboard generated!")
