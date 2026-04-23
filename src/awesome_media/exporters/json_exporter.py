import json
from awesome_media.exporters.base import BaseExporter, console


class JsonExporter(BaseExporter):
    def export(self, sources):
        path = self.output_dir / "data.json"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(
                [self._serialize(s) for s in sources], f, indent=2, ensure_ascii=False
            )
        console.print(f"[green]✓[/green] Exported {len(sources)} sources to data.json")

    def _serialize(self, source):
        return {
            "title": source.title,
            "category": source.category,
            "media_type": source.media_type,
            "country": source.country,
            "language": source.language,
            "description": source.description,
            "website_url": source.website_url,
            "rss_url": source.rss_url,
            "tags": source.tags,
        }
