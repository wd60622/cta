black:
	pipenv run black cta scripts tests setup.py

test:
	pipenv run pytest
