env:
	python3 -m venv .

install:
	pip3 install -r requirements.txt

tests:
	python3 -m unittest

style:
	pycodestyle . --exclude=./lib

sort:
	isort -rc . -s ./lib
