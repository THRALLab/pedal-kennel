.PHONY: docs tests

docs:
	cd docs && make html

tests:
	python -m unittest discover -s tests/

verbose_tests:
	python -m unittest discover -s tests/ -v
    
coverage:
	coverage run --source=. -m unittest discover -s tests/
	coverage html -i
	coverage report
	echo "HTML version available at ./htmlcov/index.html"