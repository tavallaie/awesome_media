# cli.py
from pathlib import Path
from rich.console import Console
from awesome_media.utils import load_sources

console = Console()
README_PATH = Path("README.md")


def generate_readme():
    sources = load_sources()
    if not sources:
        console.print("[red]No sources found.[/red]")
        return

    header = """# Awesome Media Catalog

| Name | Type | Country | Website | RSS |
|------|------|---------|---------|-----|
"""
    rows = []
    for s in sources:
        rss = "[Feed]({})".format(s["rss_url"]) if s["rss_url"] else "No"
        web = "[Link]({})".format(s["website_url"]) if s["website_url"] else "No"
        rows.append(
            f"| {s['title']} | {s['media_type']} | {s['country']} | {web} | {rss} |"
        )

    with open(README_PATH, "w") as f:
        f.write(header + "\n".join(rows))

    console.print("[green]✓ README.md generated[/green]")


if __name__ == "__main__":
    generate_readme()
