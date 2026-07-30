default: install

install:
	python3 adapters/claude-code/install.py

uninstall:
	python3 adapters/claude-code/install.py --remove

# N limits how many injections are listed. Empty means the script's own default.
injections:
	python3 adapters/claude-code/list_injected_modes.py $(N)
