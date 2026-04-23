# =============================================
# Awesome Media Catalog - Makefile
# =============================================

# Use 'uv run' to execute commands within the project environment
UV := uv run

# Export PYTHONPATH so Python can find the 'src' module
export PYTHONPATH := src

.PHONY: help build serve clean fix-names validate-rss all run

help:
	@echo "Available targets:"
	@echo "  build           - Fast build (skips RSS validation)"
	@echo "  validate-rss    - Check RSS links and comment out invalid ones (Slow)"
	@echo "  fix-names       - Rename YAML files to match their URLs"
	@echo "  serve           - Build and start local web server"
	@echo "  clean           - Remove output directory"

# ====================== Main Targets ======================

# Standard build: skips network checks (fast)
build: fix-names
	@mkdir -p output
	$(UV) python -m awesome_media.main

# Maintenance: Runs the heavy network checks locally
validate-rss:
	$(UV) python scripts/validate_rss.py

fix-names:
	$(UV) python scripts/rename_mismatched_files.py

serve: build
	@echo "========================================"
	@echo "Site built successfully!"
	@echo "Starting local server at http://localhost:8000"
	@echo "Press Ctrl+C to stop"
	@echo "========================================"
	cd output && $(UV) python -m http.server 8000

clean:
	rm -rf output
	@echo "✅ Cleaned output directory"

# ====================== Aliases ======================

all: build
run: serve