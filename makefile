install:
	poetry install
	
reinstall-poetry:
	rm -rf poetry.lock
	rm -rf .venv
	rm -rf ~/.cache/pypoetry/cache

install_all: install install_lhcpiv

reinstall_all: reinstall-poetry install_all

test:
	python3 -m pytest -vv src/lhcpiv/DLT_2D.py

lint:
	pylint --disable=R,C */*.py --ignore-paths=video2calibration/,pipelines/

push_commits:
	git commit -m "$(commit)" && git push
