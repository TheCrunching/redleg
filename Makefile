files := src/redleg/__init__.py src/redleg/__main__.py src/redleg/ledger.py src/redleg/tui.py src/redleg/ui.py

dist: $(files) # The target for the dist file
	./build.sh

install: dist # Install what we just created
	pip install .
