import os
import argparse
import markdown
from jinja2 import Environment, FileSystemLoader
import sys


def parse_args():
    parser = argparse.ArgumentParser(description="Convert Markdown maths notes to HTML.")
    parser.add_argument("--file", type=str, help="Convert a single Markdown file")
    parser.add_argument("--input", type=str, default="notes", help="Input folder containing .md files (default: notes/)")
    parser.add_argument("--output", type=str, default="site", help="Output folder for .html files (default: site/)")
    return parser.parse_args()

# Error reporting
def error(msg):
    print(f"Error: {msg}")
    sys.exit(1)

def convert_file(input_path, output_path, template_path, title="Chalkdust Note"):
    # Read Markdown
    with open(input_path, "r", encoding="utf-8") as f:
        md_content = f.read()
    html_content = markdown.markdown(md_content, extensions=["fenced_code", "codehilite"])

    # Load template
    env = Environment(loader=FileSystemLoader(template_path))
    template = env.get_template("base.html")

    # Render page
    rendered = template.render(title=title, content=html_content)

    # Save output
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(rendered)
    print(f"Converted: {input_path} → {output_path}")

if __name__ == "__main__":
    args = parse_args()

    # Check if single file mode
    if args.file:
        if not os.path.isfile(args.file):
            error(f"Input file not found: {args.file}")

        if not os.path.isdir("templates") or not os.path.isfile("templates/base.html"):
            error("Template not found at 'templates/base.html'")

        filename = os.path.splitext(os.path.basename(args.file))[0] + ".html"
        output_file = os.path.join(args.output, filename)
        convert_file(args.file, output_file, template_path="templates")

    else:
        # Folder mode
        input_dir = args.input or "notes"
        output_dir = args.output or "site"

        if not os.path.isdir(input_dir):
            error(f"Input folder not found: {input_dir}")

        if not os.path.isdir("templates") or not os.path.isfile("templates/base.html"):
            error("Template not found at 'templates/base.html'")

        md_files = [f for f in os.listdir(input_dir) if f.endswith(".md")]
        if not md_files:
            error(f"No .md files found in '{input_dir}'")

        print(f"Converting {len(md_files)} files in '{input_dir}' → '{output_dir}'")

        for filename in md_files:
            input_path = os.path.join(input_dir, filename)
            output_filename = os.path.splitext(filename)[0] + ".html"
            output_path = os.path.join(output_dir, output_filename)
            convert_file(input_path, output_path, template_path="templates")
