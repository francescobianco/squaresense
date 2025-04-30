
push:
	@git add .
	@git commit -am "New release!"
	@git push


test-python:
	@python3 -m sdk.python.parse-log fixtures/dataset/synthetic/e2e4.log
