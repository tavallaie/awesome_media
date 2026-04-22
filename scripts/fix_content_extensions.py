from pathlib import Path
import yaml
from urllib.parse import urlparse

CONTENTS_DIR = Path("contents")


def clean_domain(url):
    if not url:
        return None
    url_str = str(url).strip().rstrip("/")
    if not url_str.startswith(("http://", "https://")):
        url_str = "https://" + url_str
    parsed = urlparse(url_str)
    domain = parsed.netloc or parsed.path.strip("/")
    domain = domain.replace("www.", "").strip("/")
    return domain


def fix_filenames():
    if not CONTENTS_DIR.exists():
        print("❌ contents/ folder not found!")
        return

    print("🔧 Step 1: Adding .yaml to files without extension...\n")
    for item in list(CONTENTS_DIR.iterdir()):
        if item.is_file() and not item.suffix and not item.name.startswith("."):
            new_name = item.name + ".yaml"
            new_path = CONTENTS_DIR / new_name
            if not new_path.exists():
                item.rename(new_path)
                print(f"   Added .yaml → {new_name}")

    print("\n🔍 Step 2: Forcing correct name based on website URL...\n")

    renamed = 0
    skipped = 0
    errors = 0

    for file in list(CONTENTS_DIR.iterdir()):
        if not file.is_file() or file.suffix.lower() not in {".yaml", ".yml"}:
            continue

        if "example" in file.name.lower():
            print(f"⏭️  Ignored example: {file.name}")
            skipped += 1
            continue

        try:
            with open(file, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)

            website = data.get("website") if data else None
            url = website.get("url") if isinstance(website, dict) else website

            if not url:
                print(f"⚠️  No URL found → {file.name}")
                skipped += 1
                continue

            domain = clean_domain(url)
            if not domain:
                print(f"⚠️  Bad URL → {file.name}")
                skipped += 1
                continue

            new_filename = f"{domain}.yaml"
            new_path = CONTENTS_DIR / new_filename

            # Force rename even if target exists (by deleting old one if different)
            if new_path.exists() and new_path != file:
                new_path.unlink()  # remove conflicting file

            if new_path != file:
                file.rename(new_path)
                print(f"✅ Renamed: {file.name} → {new_filename}")
                renamed += 1
            else:
                print(f"✅ Correct: {file.name}")
                skipped += 1

        except Exception as e:
            print(f"❌ Error {file.name}: {e}")
            errors += 1

    print("\n" + "=" * 80)
    print(f"✅ FINISHED!")
    print(f"   Renamed : {renamed}")
    print(f"   Skipped : {skipped}")
    print(f"   Errors  : {errors}")
    print("=" * 80)


if __name__ == "__main__":
    fix_filenames()
