docker-build-dev:
	docker build -t vsu-sentiment:dev -f Dockerfile .

docker-run-dev:
	docker run -it --rm -p 8080:8080 -p 9191:9191 -v $(CURDIR):/app vsu-sentiment:dev $(cmd)
