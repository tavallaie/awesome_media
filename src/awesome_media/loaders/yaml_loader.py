import yaml
from rich.console import Console
from awesome_media.config import CONTENT_DIR
from awesome_media.models.source import Source

console = Console()


class YamlLoader:
    def load(self):
        sources = []
        if not CONTENT_DIR.exists():
            console.print("[red]Error:[/red] 'contents' directory not found.")
            return []

        yaml_files = sorted(CONTENT_DIR.glob("*.yaml"))

        for file in yaml_files:
            if file.name.lower().startswith("example"):
                continue

            try:
                with open(file, "r", encoding="utf-8") as f:
                    data = yaml.safe_load(f)

                if not data:
                    continue

                source = Source(file, data)

                # Perform validation (including filename check)
                if source.validate():
                    sources.append(source)
                else:
                    console.print(
                        f"[yellow]Skipping {file.name}:[/yellow] {source.get_errors()}"
                    )

            except Exception as e:
                console.print(f"[red]Error loading {file.name}:[/red] {e}")

        return sorted(sources, key=lambda x: x.title.lower())
