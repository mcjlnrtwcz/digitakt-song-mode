env:
	python3 -m venv .venv

install:
	pip3 install -r requirements.txt

install_dev:
	pip3 install -r requirements-dev.txt

upgrade:
	pip3 install -r requirements.txt --upgrade

style:
	pycodestyle . --exclude=.venv/lib

sort:
	isort -rc . -s .venv/lib
