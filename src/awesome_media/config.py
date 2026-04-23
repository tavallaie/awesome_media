from pathlib import Path

# --- Paths ---
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
CONTENT_DIR = ROOT_DIR / "contents"
OUTPUT_DIR = ROOT_DIR / "output"
TEMPLATE_DIR = ROOT_DIR / "templates"
README_PATH = ROOT_DIR / "index.md"

OUTPUT_DIR.mkdir(exist_ok=True, parents=True)

# --- Validation Rules ---
REQUIRED_FIELDS = ["title", "category", "country", "language", "website"]

# Expanded list of allowed tags based on your current content
ALLOWED_TAGS = [
    # Business Models
    "free",
    "paid",
    # Core Topics
    "politics",
    "governance",
    "diplomacy",
    "policy",
    "elections",
    "economy",
    "finance",
    "markets",
    "crypto",
    "startups",
    "gadgets",
    "technology",
    "ai",
    "software",
    "cybersecurity",
    "hardware",
    "science",
    "space",
    "environment",
    "medicine",
    "biotech",
    "entertainment",
    "movies",
    "music",
    "gaming",
    "arts",
    "sports",
    "football",
    "basketball",
    "esports",
    "olympics",
    "society",
    "education",
    "health",
    "lifestyle",
    "travel",
    "human-rights",
    "religion",
    # Formats & Types
    "guide",
    "tutorial",
    "whitepaper",
    "case-study",
    "documentation",
    "video",
    "podcast",
    "infographic",
    "interview",
    "analysis",
    "tool",
    "template",
    "reference",
    "faq",
    "opinion",
    # Scope & Context
    "global",
    "local",
    "trending",
    "evergreen",
    "breaking",
    "historical",
    "forecast",
    "research",
    "review",
    "deep-dive",
    # Countries (Based on error logs)
    "iran",
    "usa",
    "united-kingdom",
    "uk",
    "germany",
    "france",
    "canada",
    "netherlands",
    "norway",
    "iraq",
    "turkey",
    "afghanistan",
    "pakistan",
    "israel",
    "saudi-arabia",
    "uae",
    "russia",
    "china",
    "syria",
    "lebanon",
    "czech-republic",
    "sweden",
    "switzerland",
    "spain",
    "italy",
    "india",
]
