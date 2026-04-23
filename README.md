Awesome Media Catalog
A curated catalog of trusted news outlets, podcasts, YouTube channels, newsletters, and independent sources.

View Live SitePython

🌐 Live Version
Visit the interactive catalog at: https://tavallaie.github.io/awesome_media/

📖 About
This is a curated list of trusted news outlets, media websites, podcasts, YouTube channels, newsletters, and independent sources. It provides a modern interface to explore these resources and easy tools to export them for your RSS reader.

The project uses a robust Object-Oriented Python architecture to validate content, enforce strict naming conventions, and generate multiple export formats from a single source of truth.

✨ Features
Strict Content Validation:
Filename Enforcement: Filenames are automatically validated against the website URL defined inside the file (e.g., https://gunaz.tv/fa must be saved as gunaz.tv.fa.yaml).
Tag Whitelisting: Tags are validated against a predefined list to ensure consistency; duplicates are automatically removed.
Multiple Exports: Automatically generates:
Interactive HTML: A modern, filterable card-grid interface.
Markdown (index.md): A static table view for GitHub rendering.
JSON: Raw data for API usage or analysis.
OPML: Import feed URLs directly into your favorite RSS reader.
Rich Filtering: Filter sources by Category, Type, Country, Language, and Tags in the web interface.
Automated Deployment: GitHub Actions automatically builds the site and updates the catalog on every push.
🚀 Getting Started
Prerequisites
Python 3.10+
uv (The fast Python package installer)
Installation & Build
Clone the repository:
git clone https://github.com/tavallaie/awesome_media.gitcd awesome_media
Install dependencies:
uv sync
Run the build:
make build
This will validate your YAML files and generate output/index.html, output/data.json, and index.md.
Run locally:
make serve
This starts a local server at http://localhost:8000.
🗂️ Project Structure
The project is refactored into a modular OOP structure:

.├── contents/                  # YAML source files (e.g., dw.com.fa-ir.yaml)├── src/                       # Python source code│   └── awesome_media/│       ├── main.py            # CLI entry point & orchestrator│       ├── config.py          # Settings & Validation rules (ALLOWED_TAGS)│       ├── models/            # Data Models (Source class)│       ├── loaders/           # Input handlers (YAML parsing)│       ├── exporters/         # Output handlers (JSON, OPML, HTML, MD)│       └── utils/             # Helper functions (URL cleaning)├── templates/                 # Jinja2 HTML templates└── output/                    # Generated static files (HTML, JSON, OPML)
📝 Adding a New Source
To add a new media source, follow these strict rules to ensure the build succeeds.

1. Naming Convention
The filename must reflect the website URL.

If URL is https://gunaz.tv/fa, the file must be named: gunaz.tv.fa.yaml
If URL is https://www.dw.com/fa-ir/, the file must be named: dw.com.fa-ir.yaml
Note: The build process will warn you and skip the file if these do not match.
2. Tags
Only tags defined in the project whitelist are allowed. Duplicates are ignored automatically. (See src/awesome_media/config.py for the full list).

Examples: politics, technology, ai, society, usa, podcast, video.
3. YAML Template
Create a new .yaml file in the contents/ folder:

yaml

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
  - analysis
4. Build
Run make build. If your filename or tags are invalid, the console will display a specific error message (in yellow) explaining what needs to be fixed.

🤖 Automation & CI/CD
The project uses GitHub Actions to handle deployment automatically.

On Push: When you push to main, the workflow runs make build.
Website Deployment: The contents of the output/ folder are pushed to the gh-pages branch via peaceiris/actions-gh-pages.
Catalog Update: The generated index.md file is committed back to the repository so the GitHub table view is always up to date.
Note: The index.md is automatically excluded from triggering a recursive build loop using [skip ci].
📄 Generated Files
index.md: A GitHub-formatted markdown table containing all sources.
output/index.html: The full interactive web application.
output/data.json: A machine-readable dump of all source data.
output/feeds.opml: A file ready to be imported into any RSS reader.
📜 License
This project is open source and available under the MIT License.