# 🌟 Awesome Media Catalog

A curated catalog of trusted news outlets, podcasts, YouTube channels, newsletters, and independent sources.

[![Live Site](https://img.shields.io/badge/Live-Website-green?style=for-the-badge&logo=github)](https://tavallaie.github.io/awesome_media/)
[![Build Status](https://img.shields.io/badge/Build-Automated-blue?style=for-the-badge&logo=github-actions)](https://github.com/tavallaie/awesome_media/actions)

## 🌐 Live Version
Visit the interactive catalog at: [https://tavallaie.github.io/awesome_media/](https://tavallaie.github.io/awesome_media/)

## 📖 About
This project provides a modern, filterable interface for discovering high-quality media resources. Unlike a simple list, this project uses a robust **Object-Oriented Python architecture** to validate content, enforce naming conventions, and generate multiple export formats from a single source of truth.

## ✨ Features
* **Strict Content Validation:**
    * **Filename Enforcement:** Filenames must match the website URL (e.g., `gunaz.tv/fa` → `gunaz.tv.fa.yaml`).
    * **Tag Whitelisting:** Prevents tag bloat. Only specific Country, Focus, and Access tags are permitted.
* **Multiple Exports:** * **Interactive HTML:** A filterable card-grid interface.
    * **Markdown (`index.md`):** A static table view for GitHub previews.
    * **JSON & OPML:** Machine-readable data and RSS import files.
* **Automated Workflow:** Includes a naming fix script and GitHub Actions for instant deployment.

## 🚀 Getting Started

### Prerequisites
* **Python 3.10+**
* **[uv](https://github.com/astral-sh/uv)** (The ultra-fast Python package installer)

### Installation & Build
1. **Clone the repository:**
   ```bash
   git clone [https://github.com/tavallaie/awesome_media.git](https://github.com/tavallaie/awesome_media.git)
   cd awesome_media
   ```

2. **Install dependencies:**
   ```bash
   uv sync
   ```

3. **Run the build:**
   The build process automatically runs `fix-names` to ensure your YAML files are named correctly before generating the site.
   ```bash
   make build
   ```

4. **Run locally:**
   ```bash
   make serve
   ```
   View the site at `http://localhost:8000`.

## 🗂️ Project Structure
```text
.
├── contents/                # YAML source files (The "Source of Truth")
├── scripts/                 # Utility scripts (e.g., auto-renaming files)
├── src/                     # Python source code
│   └── awesome_media/
│       ├── main.py          # Orchestrator
│       ├── config.py        # ALLOWED_TAGS & validation rules
│       ├── models/          # Data Models (Source class)
│       └── exporters/       # HTML, JSON, OPML, and MD logic
├── templates/               # Jinja2 HTML templates
└── output/                  # Generated static files (HTML, JSON, OPML)
```

## 📝 Adding a New Source

To add a new media source, create a `.yaml` file in the `contents/` folder following these rules:

### 1. Naming Convention
The filename **must** reflect the URL to pass validation. 
* **URL:** `https://www.dw.com/fa-ir/` → **File:** `dw.com.fa-ir.yaml`
* **URL:** `https://iranintl.com` → **File:** `iranintl.com.yaml`
> **Pro Tip:** If you aren't sure, just run `make build`; the `fix-names` script will attempt to rename mismatched files for you.

### 2. Allowed Tags
To maintain a clean catalog, we only allow three types of tags:
* **Country Names:** e.g., `iran`, `usa`, `germany`, `netherlands`.
* **Focus Area:** e.g., `human-rights`, `gadgets`, `religion`, `politics`.
* **Access:** `free` or `paid`.

### 3. YAML Template
```yaml
title: "Example News"
category: "News Website"
country: "Global"
language: "Persian"
website:
  url: "[https://example.com](https://example.com)"
  text: "Visit Website"
media_type: "Digital"
description: "Brief description of the source."
rss_feed: "[https://example.com/feed.xml](https://example.com/feed.xml)"
tags:
  - iran
  - human-rights
  - free
```

## 🤖 Automation & CI/CD
The project uses **GitHub Actions**:
1.  **On Push:** Validates all files and runs the build.
2.  **Deployment:** Pushes the `output/` folder to the `gh-pages` branch.
3.  **Sync:** Commits the updated `index.md` back to `main` so the repository landing page is always current.

## 📜 License
This project is open-source and available under the **MIT License**.
