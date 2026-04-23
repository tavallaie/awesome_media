# Awesome Media Catalog

A curated catalog of trusted news outlets, podcasts, YouTube channels, newsletters, and independent sources.

[![View Live Site](https://img.shields.io/badge/View-Live%20Site-blue)](https://tavallaie.github.io/awesome_media/)
[![Python](https://img.shields.io/badge/Python-3.10+-green.svg)](https://www.python.org/)

## 🌐 Live Version
Visit the interactive catalog at: **[https://tavallaie.github.io/awesome_media/](https://tavallaie.github.io/awesome_media/)**

## 📖 About
This is a curated list of trusted news outlets, media websites, podcasts, YouTube channels, newsletters, and independent sources. It provides a modern interface to explore these resources and easy tools to export them for your RSS reader.



## ✨ Features
*   **YAML Content Management:** Add sources easily via YAML files in the `contents/` directory.
*   **Multiple Exports:** Automatically generates:
    *   **Interactive HTML:** A modern, filterable card-grid interface.
    *   **Markdown (`index.md`):** A static table view for GitHub rendering.
    *   **JSON:** Raw data for API usage or analysis.
    *   **OPML:** Import feed URLs directly into your favorite RSS reader.
*   **Rich Filtering:** Filter sources by Category, Type, Country, Language, and Tags in the web interface.
*   **Automated Deployment:** GitHub Actions automatically builds the site and updates the catalog on every push.

## 🚀 Getting Started

### Prerequisites
*   Python 3.10+
*   [uv](https://github.com/astral-sh/uv) (The fast Python package installer)

### Installation & Build

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/tavallaie/awesome_media.git
    cd awesome_media
    ```

2.  **Install dependencies:**
    ```bash
    uv sync
    ```

3.  **Run the build:**
    ```bash
    make build
    ```
    This will generate `output/index.html`, `output/data.json`, and `index.md`.

4.  **Run locally:**
    ```bash
    make serve
    ```
    This starts a local server at `http://localhost:8000`.

## 🗂️ Project Structure

```text
.
├── contents/           # YAML source files (e.g., reuters.yaml)
├── src/               # Python source code
│   └── awesome_media/
│       ├── generator.py  # Static site generator logic
│       └── utils.py    # YAML parser and normalizer
├── templates/         # Jinja2 HTML templates
└── output/            # Generated static files (HTML, JSON, OPML)
```

## 📝 Adding a New Source

1.  Create a new `.yaml` file in the `contents/` folder (or copy `example.yaml`).
2.  Use the following format:

```yaml
title: "Source Name"
category: "Technology"
country: "USA"
language: "English"
website:
  url: "https://example.com"
  text: "Visit Website"
media_type: "Podcast"
description: "A brief description of the source."
rss_feed: "https://example.com/feed.xml"
tags:
  - tech
  - ai
```

3.  Run `make build` to regenerate the site and the `index.md` list.

## 🤖 Automation & CI/CD

The project uses **GitHub Actions** to handle deployment automatically.

1.  **On Push:** When you push to `main`, the workflow runs `make build`.
2.  **Website Deployment:** The contents of the `output/` folder are pushed to the `gh-pages` branch via `peaceiris/actions-gh-pages`.
3.  **Catalog Update:** The generated `index.md` file is committed back to the repository so the GitHub table view is always up to date.

*   *Note:* The `index.md` is automatically excluded from triggering a recursive build loop using `[skip ci]`.

## 📄 Generated Files

*   **[index.md](index.md)**: A GitHub-formatted markdown table containing all sources.
*   **`output/index.html`**: The full interactive web application.
*   **`output/data.json`**: A machine-readable dump of all source data.
*   **`output/feeds.opml`**: A file ready to be imported into any RSS reader.

## 📜 License
This project is open source and available under the MIT License.
