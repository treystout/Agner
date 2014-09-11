clean:
	find . -name "*.pyc" -exec rm {} \;
	find . -name "*.pyo" -exec rm {} \;
	rm -rf ./build
	rm -rf ./dist
