from IPython.display import HTML

# Define the tasks and dependencies
task_descriptions = [
    "Define required data points",
    "Specify telemetry data source",
    "Specify time range",
    "Initiate data collection",
    "Validate minimum data points",
    "Flag missing/null values",
    "Flag out-of-range values",
    "Flag non-sequential timestamps",
    "Clean/impute invalid records",
    "Order route data",
    "Check for predefined routes",
    "Collect historical data",
    "Clean historical data",
    "Cluster historical routes",
    "Calculate normal profiles",
    "Segment current routes",
    "Calculate segment distance",
    "Calculate segment time delta",
    "Calculate segment speed",
    "Calculate heading change",
    "Identify stop events",
    "Record stop duration/location",
    "Determine time of day",
    "Determine day of week",
    "Match route to pattern",
    "Calculate cross-track error",
    "Find large deviations",
    "Aggregate route deviation events",
    "Record deviation details",
    "Compare segment speed to expected",
    "Detect speed exceedance",
    "Detect speed under-threshold",
    "Aggregate speed anomalies",
    "Record speed anomaly details",
    "Check stop location proximity",
    "Detect unexpected stops",
    "Detect over-duration stops",
    "Record stop anomalies",
    "Calculate route duration",
    "Compare to expected duration",
    "Detect total route deviation",
    "Record route duration anomaly",
    "Consolidate all anomalies",
    "Prioritize anomalies",
    "Generate structured anomaly list",
    "Present final anomalies"
]

dependencies =  [('0', []), ('1', []), ('2', []), ('3', [0, 1, 2]), ('4', [0, 3]), ('5', [4]), ('6', [4]), ('7', [4]), ('8', [5, 6, 7]), ('9', [8]), ('10', []), ('11', [10]), ('12', [0, 11]), ('13', [12]), ('14', [13]), ('15', [9]), ('16', [15]), ('17', [15]), ('18', [16, 17]), ('19', [15]), ('20', [18]), ('21', [20]), ('22', [9]), ('23', [9]), ('24', [9, 14]), ('25', [15, 24]), ('26', [25]), ('27', [26]), ('28', [27]), ('29', [18, 22, 23]), ('30', [29]), ('31', [29]), ('32', [30, 31]), ('33', [32]), ('34', [21]), ('35', [34]), ('36', [21, 34]), ('37', [35, 36]), ('38', [9]), ('39', [22, 23, 24, 38]), ('40', [39]), ('41', [40]), ('42', [28, 33, 37, 41]), ('43', [19, 42]), ('44', [43]), ('45', [44])]
mermaid_graph = ["graph TD"]
for i, desc in enumerate(task_descriptions):
    mermaid_graph.append(f'T{i}["{i}. {desc}"]')
for node, deps in dependencies:
    for dep in deps:
        mermaid_graph.append(f"T{dep} --> T{node}")

mermaid_code = "\n".join(mermaid_graph)

# HTML template with Mermaid.js from CDN
html_template = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Mermaid Task Dependency Graph</title>
    <script type="module">
      import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
      mermaid.initialize({{ startOnLoad: true }});
    </script>
</head>
<body>
    <div class="mermaid">
{mermaid_code}
    </div>
</body>
</html>
"""

# Save to file
with open("graph.html", "w", encoding="utf-8") as f:
    f.write(html_template)

print("✅ Mermaid graph exported to 'graph.html'. You can now open it in your browser.")
