# =============================================
# Awesome Media Catalog - Makefile
# =============================================

# Use 'uv run' to execute commands within the project environment
UV := uv run

# Export PYTHONPATH so Python can find the 'src' module
export PYTHONPATH := src

.PHONY: help build serve clean fix-extensions all run

help:
	@echo "Available targets:"
	@echo "  build           - Generate README.md + output/index.html"
	@echo "  fix-extensions  - Automatically add .yaml to files in contents/"
	@echo "  serve           - Build and start local web server"
	@echo "  clean           - Remove output directory"

# ====================== Main Targets ======================

build: fix-extensions
	$(UV) python -m awesome_media.generator

fix-extensions:
	$(UV) python scripts/fix_content_extensions.py

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