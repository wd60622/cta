format: 
	pipenv run black cta scripts tests setup.py

test:
	pipenv run pytest

cov:
	pipenv run pytest --cov-report html --cov cta tests && open htmlcov/index.html
