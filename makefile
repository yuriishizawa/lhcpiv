install:
	poetry install

reinstall-poetry:
	rm -rf poetry.lock
	rm -rf .venv
	rm -rf ~/.cache/pypoetry/cache
	rm -rf ~/.cache/pypoetry/virtualenvs

reinstall_all: reinstall-poetry install

test:
	python3 -m pytest -vv src/lhcpiv/DLT_2D.py

lint:
	pylint --disable=R,C */*.py --ignore-paths=video2calibration/,pipelines/

push_commits:
	git commit -m "$(commit)" && git push
