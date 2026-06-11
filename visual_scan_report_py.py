# -*- coding: utf-8 -*-
"""visual_scan_report.py



Original file is located at
    https://colab.research.google.com/drive/1OTIVtPGWIxRQ6M_w6jWqQqJLMC4LR80l
"""

# Install dependencies
!pip -q install jinja2 plotly

import os
from jinja2 import Template
import plotly.express as px

# -------------------------
# MOCK SCAN DATA
# -------------------------
results = [
    {"port": 22, "service": "ssh"},
    {"port": 80, "service": "http"},
    {"port": 443, "service": "https"},
    {"port": 3389, "service": "rdp"}
]

# -------------------------
# RISK CALCULATION
# -------------------------
high_risk_ports = {21, 23, 445, 3389}

score = 0
for item in results:
    if item["port"] in high_risk_ports:
        score += 3
    else:
        score += 1

if score >= 8:
    risk = "High"
elif score >= 4:
    risk = "Medium"
else:
    risk = "Low"

# -------------------------
# CHART
# -------------------------
ports = [str(x["port"]) for x in results]

fig = px.pie(
    names=ports,
    title="Open Ports Distribution"
)

chart_html = fig.to_html(full_html=False)

# -------------------------
# HTML TEMPLATE
# -------------------------
html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Visual Scan Report</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 40px;
            background-color: #f4f4f4;
        }

        h1 {
            color: #222;
        }

        .risk {
            font-size: 22px;
            font-weight: bold;
        }

        table {
            border-collapse: collapse;
            width: 100%;
            background: white;
        }

        th, td {
            border: 1px solid #ddd;
            padding: 10px;
        }

        th {
            background: #222;
            color: white;
        }
    </style>
</head>
<body>

<h1>Visual Scan Report</h1>

<p class="risk">Risk Level: {{ risk }}</p>

<h2>Detected Services</h2>

<table>
<tr>
<th>Port</th>
<th>Service</th>
</tr>

{% for item in results %}
<tr>
<td>{{ item.port }}</td>
<td>{{ item.service }}</td>
</tr>
{% endfor %}

</table>

<br><br>

{{ chart|safe }}

</body>
</html>
"""

# -------------------------
# RENDER REPORT
# -------------------------
template = Template(html_template)

html = template.render(
    results=results,
    risk=risk,
    chart=chart_html
)

with open("visual_scan_report.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Report generated successfully!")
print("File: visual_scan_report.html")

from google.colab import files
files.download("visual_scan_report.html")
