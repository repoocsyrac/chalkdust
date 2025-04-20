import os
import argparse
import markdown
from jinja2 import Environment, FileSystemLoader

def parse_args():
    parser = argparse.ArgumentParser(description="Convert Markdown maths notes to HTML.")
    parser.add_argument("--file", type=str, help="Convert a single Markdown file")
    parser.add_argument("--input", type=str, default="notes", help="Input folder containing .md files (default: notes/)")
    parser.add_argument("--output", type=str, default="site", help="Output folder for .html files (default: site/)")
    return parser.parse_args()

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

    if args.file:
        # Use --file mode
        input_file = args.file
        filename = os.path.splitext(os.path.basename(input_file))[0] + ".html"
        output_file = os.path.join(args.output, filename)
        convert_file(input_file, output_file, template_path="templates")
    else:
        print("todo")
        #TODO: folder mode