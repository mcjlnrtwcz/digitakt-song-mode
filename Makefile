install:
	pipenv install

install_dev:
	pipenv install -d

update:
	pipenv update

uninstall:
	pipenv --rm

start:
	pipenv run python3.6 digitakt-song-mode.py

shell:
	pipenv shell --fancy

format:
	pipenv run black .

sort:
	pipenv run isort -rc .

lint:
	pipenv run flake8 .
