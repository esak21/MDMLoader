.PHONY: build-image run-image
build-image:
	docker build -t my-python-app:latest .
run-image:
	docker run -p 8000:8000 my-python-app:latest
