PY := uv run

.PHONY: help build serve clean _serve_internal

help:
	@echo "Available targets:"
	@echo "  build   - Generate README.md and output/index.html"
	@echo "  serve   - Start a local web server and open the site"
	@echo "  clean   - Remove output directory"

build:
	PYTHONPATH=src $(PY) python -m awesome_media.generator

# Internal target to run the server
_serve_internal:
	cd output && $(PY) python -m http.server 8000

serve: build
	@echo "Starting local server at http://localhost:8000 ..."
	@echo "Press Ctrl+C to stop the server."
	# Start server in background
	@$(MAKE) _serve_internal &
	# Wait briefly for server to start
	@sleep 2
	# Open browser based on OS
	@if command -v xdg-open >/dev/null 2>&1; then \
		xdg-open http://localhost:8000; \
	elif command -v open >/dev/null 2>&1; then \
		open http://localhost:8000; \
	else \
		echo "Server running at http://localhost:8000 (open manually)"; \
	fi
	# Bring the background job to foreground so Ctrl+C works
	@wait

clean:
	rm -rf output