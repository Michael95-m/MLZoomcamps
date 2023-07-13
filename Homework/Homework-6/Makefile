setup:
	pipenv install --dev

quality_check:
	isort .
	black .
	pylint --recursive=y .

test: quality_check
	pytest tests

integration_test: test
	./integration_test.sh

