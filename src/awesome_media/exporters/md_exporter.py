from awesome_media.exporters.base import BaseExporter, console
from awesome_media.config import README_PATH
from awesome_media.utils.strings import truncate_text


class MarkdownExporter(BaseExporter):
    def export(self, sources):
        header = """# Awesome Media Catalog

A curated catalog of trusted news outlets, podcasts, YouTube channels, newsletters, and independent sources.

[![View Web Version](https://img.shields.io/badge/View-Web%20Version-blue)](https://tavallaie.github.io/awesome_media/)

## 📰 Catalog

| Name | Type | Country | Language | Website | RSS | Description |
|------|------|---------|----------|---------|-----|-------------|
"""
        rows = []
        for s in sources:
            web_link = (
                f"[{s.website_text}]({s.website_url})" if s.website_url else "N/A"
            )
            rss_link = f"[Feed]({s.rss_url})" if s.rss_url else "❌"
            desc = truncate_text(s.description, 120)

            row = f"| {s.title} | {s.media_type} | {s.country} | {s.language} | {web_link} | {rss_link} | {desc} |\n"
            rows.append(row)

        with open(README_PATH, "w", encoding="utf-8") as f:
            f.write(header + "".join(rows))

        console.print("[bold green]✓[/bold green] index.md generated")
