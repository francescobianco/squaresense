
push:
	@git add .
	@git commit -am "New release!"
	@git push


sample:
	@echo "Ctrl + A, Ctrl + X to stop"
	@sudo picocom -b 230400 /dev/ttyUSB0 > fixtures/dataset/samples/sample0.log

debug-serial:
	@echo "Ctrl + C to stop"
	@sudo python3 -m sdk.python.debug-serial

test-python:
	@#python3 -m sdk.python.parse-log fixtures/dataset/synthetic/e2e4.log
	@python3 -m sdk.python.parse-log fixtures/dataset/samples/sample0.log
