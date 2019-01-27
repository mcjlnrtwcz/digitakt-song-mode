install:
	pipenv install

install_dev:
	pipenv install -d

uninstall:
	pipenv --rm

shell:
	pipenv shell

start:
	pipenv run python3.6 digitakt-song-mode.py

style:
	pipenv run pycodestyle .

sort:
	pipenv run isort -rc .
