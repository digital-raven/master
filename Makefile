all:
	cd ./docs/man && make
	python3 -m build

release:
	twine upload -r pypi dist/*

clean:
	rm -rf master.egg-info dist/ docs/man/*.gz
