import os
import argparse
import markdown
from jinja2 import Environment, FileSystemLoader
import sys
import logging
from datetime import datetime


def parse_args():
    parser = argparse.ArgumentParser(description="Convert Markdown maths notes to HTML.")
    parser.add_argument("--file", type=str, help="Convert a single Markdown file")
    parser.add_argument("--input", type=str, default="notes", help="Input folder containing .md files (default: notes/)")
    parser.add_argument("--output", type=str, default="site", help="Output folder for .html files (default: site/)")
    parser.add_argument("--title", type=str, help="Custom title for a single note")
    # Mutually exclusive group for overwrite options
    overwrite_group = parser.add_mutually_exclusive_group()
    overwrite_group.add_argument("--no-overwrite", action="store_true", help="Skip files that already exist")
    overwrite_group.add_argument("--force", action="store_true", help="Force overwriting of existing output files (default behaviour)")
    # Mutually exclusive group for verbosity options
    verbosity = parser.add_mutually_exclusive_group()
    verbosity.add_argument("--quiet", action="store_true", help="Suppress most terminal output")
    verbosity.add_argument("--verbose", action="store_true", help="Show extra terminal output (debug level)")

    return parser.parse_args()

# Error reporting
def error(msg):
    logging.error(f"❌ {msg}")
    sys.exit(1)

# Logging
def setup_logging(quiet=False, verbose=False):
    os.makedirs("logs", exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    logfile = f"logs/build_{timestamp}.log"

    log_level_console = logging.WARNING if quiet else logging.DEBUG if verbose else logging.INFO

    # Create logger
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(logfile, encoding="utf-8")
        ]
    )

    # Add console handler with dynamic verbosity
    console = logging.StreamHandler()
    console.setLevel(log_level_console)
    console.setFormatter(logging.Formatter("%(message)s"))
    logging.getLogger().addHandler(console)

    logging.info("Logging started")


def convert_file(input_path, output_path, template_path, title="Chalkdust Note"):
    # Read Markdown
    with open(input_path, "r", encoding="utf-8") as f:
        md_content = f.read()
    html_content = markdown.markdown(md_content, extensions=["fenced_code", "codehilite"])

    # Load template
    env = Environment(loader=FileSystemLoader(template_path))
    template = env.get_template("base.html")

    template_path_file = os.path.join(template_path, "base.html")
    with open(template_path_file, "r", encoding="utf-8") as f:
        template_source = f.read()
        if "{{ content" not in template_source:
            logging.error("Template is missing a '{{ content }}' placeholder.")
            return

    # Render page
    rendered = template.render(title=title, content=html_content)

    # Save output
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(rendered)
    logging.info(f"Converted: {input_path} → {output_path}")

if __name__ == "__main__":
    args = parse_args()
    setup_logging(quiet=args.quiet, verbose=args.verbose)

    if args.file and args.input != "notes":
        logging.warning("⚠️ --file and --input were both provided. Using --file and ignoring --input.")

    # Check if single file mode
    if args.file:
        if not os.path.isfile(args.file):
            error(f"Input file not found: {args.file}")

        if not os.path.isdir("templates") or not os.path.isfile("templates/base.html"):
            error("Template not found at 'templates/base.html'")

        with open(args.file, "r", encoding="utf-8") as f:
            content = f.read()
            if not content.strip():
                logging.warning(f"⚠️ Skipping empty file: {args.file}")
                sys.exit(0)

        filename = os.path.splitext(os.path.basename(args.file))[0] + ".html"
        output_file = os.path.join(args.output, filename)

        if args.no_overwrite and os.path.exists(output_file):
            logging.info(f"⏭️  Skipped (already exists): {output_file}")
            sys.exit(0)
        convert_file(args.file, output_file, template_path="templates", title=args.title or "Chalkdust Note")

    else:
        # Folder mode
        if args.title:
            logging.warning("⚠️ --title will be ignored when using --input (folder mode).")

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

        converted = 0
        skipped = 0
        errors = 0

        for filename in md_files:
            input_path = os.path.join(input_dir, filename)
            output_filename = os.path.splitext(filename)[0] + ".html"
            output_path = os.path.join(output_dir, output_filename)
            title = os.path.splitext(filename)[0].replace("-", " ").replace("_", " ").title()
            try:
                if not os.path.isfile(input_path):
                    logging.warning(f"⚠️ Skipping missing file: {input_path}")
                    skipped += 1
                    continue

                # Check for empty markdown file
                with open(input_path, "r", encoding="utf-8") as f:
                    if not f.read().strip():
                        logging.warning(f"⚠️ Skipping empty file: {input_path}")
                        skipped += 1
                        continue

                # Convert file
                if args.no_overwrite and os.path.exists(output_path):
                    logging.info(f"⏭️  Skipped (already exists): {output_path}")
                    skipped += 1
                    continue

                convert_file(input_path, output_path, template_path="templates", title=title)
                converted += 1

            except Exception as e:
                logging.error(f"Failed to convert {input_path}: {e}")
                errors += 1

        logging.info(f"✅ Done: {converted} converted, {skipped} skipped, {errors} errors.")
