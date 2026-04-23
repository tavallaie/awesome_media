import yaml
import sys
from pathlib import Path

# Add src to path to import our utils
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from awesome_media.utils.strings import url_to_filename

CONTENT_DIR = Path(__file__).parent.parent / "contents"


def main():
    print("🔍 Checking filenames against URLs...")

    yaml_files = sorted(CONTENT_DIR.glob("*.yaml"))
    renamed_count = 0

    for file in yaml_files:
        if file.name.startswith("example"):
            continue

        try:
            with open(file, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)

            if not data:
                continue

            # Get URL
            web = data.get("website")
            if isinstance(web, dict):
                url = web.get("url")
            elif isinstance(web, str):
                url = web
            else:
                url = None

            if not url:
                continue

            # Calculate expected name
            expected_name = url_to_filename(url)

            # Check mismatch
            if expected_name and file.name != expected_name:
                old_path = file
                new_path = CONTENT_DIR / expected_name

                print(f"Renaming: {file.name} -> {expected_name}")

                # Perform rename
                # Avoid conflict if target already exists
                if new_path.exists():
                    print(f"  ⚠️  Skipped: Target {expected_name} already exists.")
                else:
                    old_path.rename(new_path)
                    renamed_count += 1

        except Exception as e:
            print(f"❌ Error processing {file.name}: {e}")

    print(f"\n✅ Done! Renamed {renamed_count} files.")


if __name__ == "__main__":
    main()
