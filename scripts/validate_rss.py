import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from awesome_media.loaders.yaml_loader import YamlLoader
from rich.console import Console

console = Console()


def main():
    rprint = console.print
    rprint("[bold blue]Validating RSS Feeds...[/bold blue]")
    rprint("This may take a while if you have many sources.\n")

    # Load sources with validation enabled
    loader = YamlLoader()
    sources = loader.load(validate_rss=True)

    # Summary
    total = len(sources)
    with_rss = len([s for s in sources if s.rss_url])

    console.print("\n[bold green]Validation Complete![/bold green]")
    console.print(f"Processed {total} valid sources.")
    console.print(f"Active RSS feeds: {with_rss}")
    console.print(f"Sources without valid RSS: {total - with_rss}")
    console.print(
        "\nInvalid links have been commented out in their respective YAML files."
    )


if __name__ == "__main__":
    main()
