# =============================================
# Awesome Media Catalog - Makefile
# =============================================

# Use 'uv run' to execute commands within the project environment
UV := uv run

# Export PYTHONPATH so Python can find the 'src' module
export PYTHONPATH := src

.PHONY: help build serve clean fix-names all run

help:
	@echo "Available targets:"
	@echo "  build           - Fix filenames and generate index.md + output/"
	@echo "  fix-names       - Rename YAML files to match their internal website URLs"
	@echo "  serve           - Build and start local web server"
	@echo "  clean           - Remove output directory"

# ====================== Main Targets ======================

# First, it runs 'fix-names' to ensure filenames match URLs, then builds
build: fix-names
	mkdir -p output
	$(UV) python -m awesome_media.main

# This target runs the script to rename files
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