from awesome_media.config import REQUIRED_FIELDS, ALLOWED_TAGS
from awesome_media.utils.strings import url_to_filename


class Source:
    def __init__(self, filepath, data):
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

        # 4. Normalize Tags (Deduplicate & Lowercase)
        raw_tags = data.get("tags", [])
        self.tags = sorted(list({str(t).strip().lower() for t in raw_tags if t}))

    def to_dict(self):
        """
        Returns a dictionary safe for JSON serialization.
        Excludes non-serializable objects like PosixPath.
        """
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
