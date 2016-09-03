IMAGE = igrishaev/vsu:sentiment

docker-build-dev:
	docker build -t $(IMAGE).dev -f Dockerfile-dev .

docker-run-dev:
	docker run -it --rm -p 8080:8080 -p 9191:9191 -v $(CURDIR):/app $(IMAGE).dev $(cmd)

docker-build-prod:
	docker build -t $(IMAGE) -f Dockerfile --no-cache .

docker-run-prod:
	docker run -it --rm -p 8080:8080 -p 9191:9191 $(IMAGE) $(cmd)

docker-push:
	docker push $(IMAGE)

get-dataset:
	wget "http://thinknook.com/wp-content/uploads/2012/09/Sentiment-Analysis-Dataset.zip"
	unzip "Sentiment-Analysis-Dataset.zip"
	rm "Sentiment-Analysis-Dataset.zip"
	mv "Sentiment Analysis Dataset.csv" "source.csv"
