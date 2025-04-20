import os
import markdown
from jinja2 import Environment, FileSystemLoader

# Paths
input_path = "notes/example.md"
output_path = "site/example.html"
template_path = "templates"
title = "Example Note"

# Load Markdown
with open(input_path, "r", encoding="utf-8") as f:
    md_content = f.read()
html_content = markdown.markdown(md_content, extensions=["fenced_code", "codehilite"])

# Load template
env = Environment(loader=FileSystemLoader(template_path))
template = env.get_template("base.html")

# Render page
rendered = template.render(title=title, content=html_content)

# Save output
os.makedirs("site", exist_ok=True)
with open(output_path, "w", encoding="utf-8") as f:
    f.write(rendered)

print(f"Generated {output_path}")
