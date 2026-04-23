from rich.console import Console
from rich.table import Table
from rich import print as rprint

from awesome_media.config import OUTPUT_DIR
from awesome_media.loaders.yaml_loader import YamlLoader
from awesome_media.exporters.json_exporter import JsonExporter
from awesome_media.exporters.opml_exporter import OpmlExporter
from awesome_media.exporters.md_exporter import MarkdownExporter
from awesome_media.exporters.html_exporter import HtmlExporter

console = Console()


def show_summary(sources):
    table = Table(title="Generated Summary")
    table.add_column("Source", style="cyan")
    table.add_column("Type", style="magenta")
    table.add_column("Country", style="yellow")
    table.add_column("Filename Check", justify="center")

    # Note: Filename check is implicitly '✅' because loader skipped invalid ones,
    # but let's show if they have RSS
    for entry in sources[:5]:
        rss = "✅" if entry.rss_url else "❌"
        c = (entry.country[:15] + "...") if len(entry.country) > 15 else entry.country
        table.add_row(entry.title, entry.media_type, c or "-", rss)

    if len(sources) > 5:
        table.add_row(f"... and {len(sources) - 5} more", "", "", "")
    console.print(table)


def main():
    rprint("[bold blue]Building Awesome Media...[/bold blue]")

    # 1. Load
    loader = YamlLoader()
    sources = loader.load()

    if not sources:
        console.print("[red]Abort:[/red] No sources found.")
        return

    console.print(f"[green]Found[/green] {len(sources)} media sources.\n")

    # 2. Summary
    show_summary(sources)
    print()

    # 3. Export
    # We inject OUTPUT_DIR to exporters
    JsonExporter(OUTPUT_DIR).export(sources)
    OpmlExporter(OUTPUT_DIR).export(sources)
    MarkdownExporter(OUTPUT_DIR).export(sources)
    HtmlExporter(OUTPUT_DIR).export(sources)

    rprint("\n[bold green]Build Complete![/bold green]")


if __name__ == "__main__":
    main()
