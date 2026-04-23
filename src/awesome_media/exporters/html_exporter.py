import json
from jinja2 import Environment, FileSystemLoader, select_autoescape
from awesome_media.exporters.base import BaseExporter, console
from awesome_media.config import TEMPLATE_DIR


class HtmlExporter(BaseExporter):
    def export(self, sources):
        if not TEMPLATE_DIR.exists():
            console.print("[red]Error:[/red] Templates directory not found.")
            return

        env = Environment(
            loader=FileSystemLoader(str(TEMPLATE_DIR)),
            autoescape=select_autoescape(["html", "xml"]),
        )
        template = env.get_template("index.html")

        # Calculate filters
        categories = sorted({s.category for s in sources})
        countries = sorted({s.country for s in sources if s.country})
        languages = sorted({s.language for s in sources if s.language})
        media_types = sorted({s.media_type for s in sources})
        all_tags = sorted({t for s in sources for t in s.tags})

        # Convert sources to dicts for JSON serialization
        sources_data = [s.to_dict() for s in sources]

        # Render template
        html_content = template.render(
            sources=sources,
            sources_json=json.dumps(sources_data),
            categories=categories,
            countries=countries,
            languages=languages,
            media_types=media_types,
            all_tags=all_tags,
        )

        with open(self.output_dir / "index.html", "w", encoding="utf-8") as f:
            f.write(html_content)

        console.print(
            f"[green]✓[/green] Generated {len(sources)} cards into output/index.html"
        )
