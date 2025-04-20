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

## 🔧 How to Use It

If you just want to use Chalkdust to build your own site (without touching the internal code):

1. Clone the repo:
   ```bash
   git clone https://github.com/repoocsyrac/chalkdust.git
   cd chalkdust
   ```

2. Install the requirements:
   ```bash
   pip install -r requirements.txt
   ```

3. Add your Markdown notes to the `notes/` folder (or another folder you choose)

4. Run the generator:
   ```bash
   python generate.py
   ```

5. Your finished HTML site will be in the `site/` folder — ready to upload, zip, or deploy anywhere (e.g. GitHub Pages, Netlify)

> Only the contents of `site/` are needed to host your website. You don’t need to copy any templates, source code, logs, or Markdown files.

---

## 🛠 CLI Usage

### Basic folder conversion:
```bash
python generate.py
```
Converts all Markdown files in `notes/` → `site/`.

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

## 🚀 Deploying to GitHub Pages

If you want to publish your generated site, just push the contents of the `site/` folder to GitHub Pages.

Recommended: output to a `docs/` folder instead and set GitHub Pages to serve from it:

```bash
python generate.py --output docs
touch docs/.nojekyll  # optional, avoids issues with MathJax
```

Then enable GitHub Pages in your repo settings:
- **Branch**: `main`
- **Folder**: `/docs`

Your site will be live at:
```
https://your-username.github.io/your-repo-name/
```

---

Happy notetaking ✏️
