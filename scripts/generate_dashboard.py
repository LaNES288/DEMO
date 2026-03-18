import pandas as pd
from datetime import datetime, timezone

# Load data
df = pd.read_csv("issues.csv")

# Convert to datetime (make it timezone-aware)
df["created_at"] = pd.to_datetime(df["created_at"], utc=True)

# Use timezone-aware current time
now = datetime.now(timezone.utc)

# Calculate age in days
df["age_days"] = (now - df["created_at"]).dt.days

# Metrics
total_issues = len(df)
avg_age = round(df["age_days"].mean(), 1) if total_issues > 0 else 0
oldest = df.sort_values("age_days", ascending=False).head(5)

assignees = df["assignee"].value_counts()

# Generate HTML
html = f"""
<html>
<head>
    <title>Backlog Dashboard</title>
</head>
<body>
    <h1>📊 Backlog Dashboard</h1>

    <h2>Summary</h2>
    <p>Total Issues: {total_issues}</p>
    <p>Average Age: {avg_age} days</p>

    <h2>👤 Issues per Assignee</h2>
    {assignees.to_frame().to_html()}

    <h2>⏳ Oldest Issues</h2>
    {oldest.to_html(index=False)}

</body>
</html>
"""

# Save dashboard
with open("docs/index.html", "w") as f:
    f.write(html)

print("Dashboard generated!")
