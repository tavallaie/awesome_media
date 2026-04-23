# src/awesome_media/utils.py
import yaml
from pathlib import Path
from rich.console import Console

console = Console()
CONTENT_DIR = Path("contents")

REQUIRED_FIELDS = ["title", "category", "country", "language", "website"]


def load_sources():
    """
    Loads and normalizes all YAML sources.
    Returns a sorted list of dictionaries.
    """
    sources = []
    if not CONTENT_DIR.exists():
        console.print("[red]Error:[/red] 'contents' directory not found.")
        return sources

    yaml_files = sorted(CONTENT_DIR.glob("*.yaml"))

    for file in yaml_files:
        # FIX: Ignore example.yaml
        if file.name.lower() == "example.yaml":
            continue

        try:
            with open(file, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)

            if not data or not data.get("title"):
                continue

            # Validate required fields
            missing = [field for field in REQUIRED_FIELDS if field not in data]
            if missing:
                console.print(
                    f"[yellow]Skipping {file.name}:[/yellow] Missing {missing}"
                )
                continue

            # Normalize Website (Handle String or Dict)
            web = data.get("website")
            website_url = ""
            website_text = "Website"
            if isinstance(web, str):
                website_url = web
            elif isinstance(web, dict):
                website_url = web.get("url", "")
                website_text = web.get("text", "Website")

            # Normalize RSS
            rss = data.get("rss_feed") or data.get("rss")
            rss_url = str(rss) if rss else ""

            # Clean description
            description = str(data.get("description", "")).replace("\n", " ").strip()

            source = {
                "title": str(data.get("title")),
                "category": str(data.get("category")),
                "media_type": str(data.get("media_type", data.get("category"))),
                "country": str(data.get("country")),
                "language": str(data.get("language")),
                "description": description,
                "website_url": website_url,
                "website_text": website_text,
                "rss_url": rss_url,
                "tags": data.get("tags", []),  # Ensure tags are loaded
            }
            sources.append(source)

        except Exception as e:
            console.print(f"[red]Error loading {file.name}:[/red] {e}")

    return sorted(sources, key=lambda x: x["title"].lower())
