# Chalkdust

**Chalkdust** is a lightweight command-line static site generator designed specifically for math notes. It converts Markdown files (with LaTeX-style math) into HTML pages using MathJax for rendering.

---

## ✨ Features
- Converts `.md` files to styled `.html` notes
- LaTeX-style math rendering via MathJax
- Optional `config.yaml` support
- Generates `index.html` to list all notes (by default)
- Smart CLI with logging, overwrite control, and verbosity levels

---

## 📦 Installation

### Requirements
- Python 3.8+
- `pip`

### Install dependencies:
```bash
pip install -r requirements.txt
```

---

## 🛠 Usage

### Basic folder conversion:
```bash
python generate.py
```
This converts all Markdown files in the `notes/` folder and outputs HTML to the `site/` folder.

### Convert a single file:
```bash
python generate.py --file notes/example.md
```

### Specify input/output folders:
```bash
python generate.py --input my_notes --output my_site
```

### Add a custom title:
```bash
python generate.py --file notes/example.md --title "Limits and Infinity"
```

### Skip overwriting existing files:
```bash
python generate.py --no-overwrite
```

### Hide `index.html` generation:
```bash
python generate.py --no-index
```

### Use a config file:
```bash
python generate.py --config config.yaml
```

---

## 🧾 Example `config.yaml`
```yaml
input: notes
output: site
template: templates
title: My Default Title
```

---

## 🎨 Customisation
You can modify the HTML style by editing:
- `templates/base.html` — the page structure
- `static/style.css` — the chalkboard-inspired theme

Supports full MathJax LaTeX for inline (`$...$`) and block (`$$...$$`) maths.

---

## 🪄 Extras
- `--version` — show version info
- `--about` — a short description of the project

---

## 📁 Folder Structure
```
chalkdust/
├── logs/               # Log files
├── notes/              # Markdown source files
├── site/               # Generated HTML output
├── templates/          # Jinja2 HTML templates
├── static/             # CSS and assets
├── generate.py         # Main CLI tool
├── config.yaml         # (Optional) config
└── requirements.txt    # Python dependencies
```

---

Happy notetaking ✏️
