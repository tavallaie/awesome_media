# src/awesome_media/generator.py
import json
import xml.etree.ElementTree as ET
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape
from rich.console import Console
from rich.table import Table
from rich import print as rprint

# Use shared loader
from awesome_media.utils import load_sources

console = Console()

# Resolve paths relative to this file
# src/awesome_media/generator.py -> go up 3 levels -> root
BASE_DIR = Path(__file__).resolve().parent.parent.parent
OUTPUT_DIR = BASE_DIR / "output"
TEMPLATE_DIR = BASE_DIR / "templates"
# CHANGED: Output to index.md instead of README.md
README_PATH = BASE_DIR / "index.md"


# --- DATA EXPORT LOGIC ---
def generate_json(sources):
    """Exports all data to output/data.json."""
    OUTPUT_DIR.mkdir(exist_ok=True)
    json_path = OUTPUT_DIR / "data.json"

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(sources, f, indent=2, ensure_ascii=False)

    console.print(f"[green]✓[/green] Exported {len(sources)} sources to data.json")


def generate_opml(sources):
    """Exports RSS feeds to output/feeds.opml for import into readers."""
    OUTPUT_DIR.mkdir(exist_ok=True)
    opml_path = OUTPUT_DIR / "feeds.opml"

    # Build XML
    opml = ET.Element("opml", version="1.0")
    head = ET.SubElement(opml, "head")
    ET.SubElement(head, "title").text = "Awesome Media Feeds"
    ET.SubElement(head, "dateCreated").text = str(Path(__file__).stat().st_mtime)

    body = ET.SubElement(opml, "body")

    # Group by category
    categories = {}
    for s in sources:
        if not s.get("rss_url"):
            continue  # Skip sources without RSS
        cat = s.get("category", "Uncategorized")
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(s)

    # Build XML Tree
    for cat_name, cat_sources in categories.items():
        cat_outline = ET.SubElement(body, "outline", text=cat_name, title=cat_name)
        for s in cat_sources:
            ET.SubElement(
                cat_outline,
                "outline",
                text=s["title"],
                title=s["title"],
                type="rss",
                htmlUrl=s["website_url"],
                xmlUrl=s["rss_url"],
            )

    # Pretty print and save
    xml_str = ET.tostring(opml, encoding="utf-8", method="xml")
    # Simple pretty print hack
    from xml.dom import minidom

    parsed = minidom.parseString(xml_str)
    pretty_xml = parsed.toprettyxml(indent="  ")

    with open(opml_path, "w", encoding="utf-8") as f:
        f.write(pretty_xml)

    console.print("[green]✓[/green] Exported OPML file for RSS readers")


# --- README GENERATOR LOGIC ---
def generate_readme(sources):
    """Generates the index.md using the loaded sources."""
    # CHANGED: Renamed Title to Awesome Media Catalog (kept your Shield badge)
    header = """# Awesome Media Catalog

A curated catalog of trusted news outlets, podcasts, YouTube channels, newsletters, and independent sources.

[![View Web Version](https://img.shields.io/badge/View-Web%20Version-blue)](https://tavallaie.github.io/awesome_media/)

## 📰 Catalog

| Name | Type | Country | Language | Website | RSS | Description |
|------|------|---------|----------|---------|-----|-------------|
"""

    rows = []
    for s in sources:
        # Format Website Link
        if s["website_url"]:
            web_link = f"[{s['website_text']}]({s['website_url']})"
        else:
            web_link = "N/A"

        # Format RSS Link
        if s["rss_url"]:
            rss_link = f"[Feed]({s['rss_url']})"
        else:
            rss_link = "❌"

        # Truncate description
        desc = s["description"].replace("\n", " ").strip()
        if len(desc) > 120:
            desc = desc[:117] + "..."

        # Fallbacks
        country = s["country"] if s["country"] else "-"
        language = s["language"] if s["language"] else "-"
        m_type = s["media_type"] if s["media_type"] else s["category"]

        row = f"| {s['title']} | {m_type} | {country} | {language} | {web_link} | {rss_link} | {desc} |\n"
        rows.append(row)

    final_content = header + "".join(rows)

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(final_content)

    console.print("[bold green]✓[/bold green] index.md generated")


# --- TABLE SUMMARY LOGIC ---
def show_summary_table(sources):
    """Displays the Rich Table summary in the terminal."""
    table = Table(title="Generated Summary")
    table.add_column("Source", style="cyan")
    table.add_column("Type", style="magenta")
    table.add_column("Country", style="yellow")
    table.add_column("Web", justify="center")
    table.add_column("RSS", justify="center")

    for entry in sources[:5]:
        w = "✅" if entry["website_url"] else "❌"
        r = "✅" if entry["rss_url"] else "❌"
        c = (
            (entry["country"][:15] + "...")
            if len(entry["country"]) > 15
            else entry["country"]
        )
        table.add_row(entry["title"], entry["media_type"], c or "-", w, r)

    if len(sources) > 5:
        table.add_row(f"... and {len(sources) - 5} more", "", "", "", "")

    console.print(table)


# --- HTML GENERATOR LOGIC ---
def generate_html(sources):
    """Generates the static site using Jinja2."""

    OUTPUT_DIR.mkdir(exist_ok=True)

    if not TEMPLATE_DIR.exists():
        console.print(
            f"[red]Error:[/red] Templates directory not found at {TEMPLATE_DIR}"
        )
        return

    # Setup Jinja2
    env = Environment(
        loader=FileSystemLoader(str(TEMPLATE_DIR)),
        autoescape=select_autoescape(["html", "xml"]),
    )

    try:
        template = env.get_template("index.html")
    except Exception as e:
        console.print(f"[red]Template Error:[/red] {e}")
        return

    # Calculate unique filter options
    categories = sorted(list({s["category"] for s in sources}))
    countries = sorted(list({s["country"] for s in sources if s["country"]}))
    languages = sorted(list({s["language"] for s in sources if s["language"]}))
    media_types = sorted(list({s["media_type"] for s in sources}))
    all_tags = sorted(list({t for s in sources for t in s.get("tags", [])}))

    # Render template
    html_content = template.render(
        sources=sources,
        sources_json=json.dumps(sources),
        categories=categories,
        countries=countries,
        languages=languages,
        media_types=media_types,
        all_tags=all_tags,
    )

    with open(OUTPUT_DIR / "index.html", "w", encoding="utf-8") as f:
        f.write(html_content)

    console.print(
        f"[green]✓[/green] Generated {len(sources)} cards into output/index.html"
    )


# --- MAIN BUILD ORCHESTRATOR ---
def main():
    rprint("[bold blue]Building Awesome Media...[/bold blue]")
    console.print("Loading sources from 'contents/'...")

    sources = load_sources()

    if not sources:
        console.print("[red]Abort:[/red] No sources found.")
        return

    console.print(f"[green]Found[/green] {len(sources)} media sources.\n")

    # 1. Show Summary
    show_summary_table(sources)

    print()  # Add a newline

    # 2. Generate Exports (JSON & OPML)
    generate_json(sources)
    generate_opml(sources)

    # 3. Generate index.md
    generate_readme(sources)

    # 4. Generate HTML
    generate_html(sources)

    rprint("\n[bold green]Build Complete![/bold green]")


if __name__ == "__main__":
    main()
