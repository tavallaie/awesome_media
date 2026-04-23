import fastfeedparser
from rich.console import Console
from awesome_media.config import REQUIRED_FIELDS, ALLOWED_TAGS
from awesome_media.utils.strings import url_to_filename

console = Console()


class Source:
    def __init__(self, filepath, data, validate_rss=False):
        self.filepath = filepath
        self.raw_data = data
        self._errors = []

        # 1. Normalize Fields
        self.title = str(data.get("title", ""))
        self.category = str(data.get("category", ""))
        self.media_type = str(data.get("media_type", self.category))
        self.country = str(data.get("country", ""))
        self.language = str(data.get("language", ""))
        self.description = str(data.get("description", ""))

        # 2. Normalize Website
        web = data.get("website")
        if isinstance(web, str):
            self.website_url = web
            self.website_text = "Visit Website"
        elif isinstance(web, dict):
            self.website_url = web.get("url", "")
            self.website_text = web.get("text", "Visit Website")
        else:
            self.website_url = ""
            self.website_text = "N/A"

        # 3. Normalize RSS
        rss = data.get("rss_feed") or data.get("rss")
        self.rss_url = str(rss) if rss else ""

        # 4. Validate RSS Link (Only if explicitly requested)
        if validate_rss and self.rss_url:
            self._validate_rss()

        # 5. Normalize Tags
        raw_tags = data.get("tags", [])
        self.tags = sorted(list({str(t).strip().lower() for t in raw_tags if t}))

    def _comment_rss_in_file(self):
        """
        Opens the YAML file on disk and comments out the invalid rss_feed line.
        """
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                lines = f.readlines()

            new_lines = []
            changed = False

            for line in lines:
                stripped = line.lstrip()
                if (
                    stripped.startswith("rss_feed:") or stripped.startswith("rss:")
                ) and not stripped.startswith("#"):
                    new_lines.append("#" + line)
                    changed = True
                else:
                    new_lines.append(line)

            if changed:
                with open(self.filepath, "w", encoding="utf-8") as f:
                    f.writelines(new_lines)
                console.print(
                    f"[dim]✎[/dim] Commented out invalid RSS in {self.filepath.name}"
                )

        except Exception as e:
            console.print(f"[red]Error updating file {self.filepath.name}: {e}[/red]")

    def _validate_rss(self):
        """
        Checks if the RSS URL is valid using fastfeedparser.
        If invalid, comments it out in the YAML file and clears self.rss_url.
        """
        try:
            # Attempt to parse the feed
            feed = fastfeedparser.parse(self.rss_url)

            # Check if we actually got a feed back
            if not feed or not feed.feed:
                raise ValueError("Empty or invalid feed structure")

        except Exception as e:
            console.print(
                f"[yellow]RSS Warning:[/yellow] Removing invalid feed for [bold]{self.title}[/bold]. "
                f"Reason: {str(e)[:60]}..."
            )

            # 1. Comment it out in the file
            self._comment_rss_in_file()

            # 2. Clear the URL so it's not exported
            self.rss_url = ""

    def to_dict(self):
        return {
            "title": self.title,
            "category": self.category,
            "media_type": self.media_type,
            "country": self.country,
            "language": self.language,
            "description": self.description,
            "website_url": self.website_url,
            "website_text": self.website_text,
            "rss_url": self.rss_url,
            "tags": self.tags,
        }

    @property
    def expected_filename(self):
        if not self.website_url:
            return None
        return url_to_filename(self.website_url)

    def validate(self):
        """Validates fields and tags. Returns True if valid."""
        # A. Check Required Fields
        missing = [f for f in REQUIRED_FIELDS if f not in self.raw_data]
        if missing:
            self._errors.append(f"Missing fields: {missing}")

        # B. Check Filename Consistency
        if self.expected_filename and self.filepath.name != self.expected_filename:
            self._errors.append(
                f"Filename mismatch! File is '{self.filepath.name}' "
                f"but URL suggests '{self.expected_filename}'"
            )

        # C. Validate Tags
        invalid_tags = [t for t in self.tags if t not in ALLOWED_TAGS]
        if invalid_tags:
            self._errors.append(
                f"Invalid tags found: {invalid_tags}. "
                f"Please use tags from the generic list."
            )

        return len(self._errors) == 0

    def get_errors(self):
        return self._errors
