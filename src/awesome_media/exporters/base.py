from abc import ABC, abstractmethod
from pathlib import Path
from rich.console import Console

console = Console()


class BaseExporter(ABC):
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir

    @abstractmethod
    def export(self, sources):
        pass
