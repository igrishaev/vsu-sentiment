docker-build-dev:
	docker build -t vsu-sentiment:dev -f Dockerfile-dev .

docker-run-dev:
	docker run -it --rm -p 8080:8080 -p 9191:9191 -v $(CURDIR):/app vsu-sentiment:dev $(cmd)

docker-build-prod:
	docker build -t vsu-sentiment:prod -f Dockerfile .

docker-run-prod:
	docker run -it --rm -p 8080:8080 -p 9191:9191 vsu-sentiment:prod $(cmd)

get-dataset:
	wget "http://thinknook.com/wp-content/uploads/2012/09/Sentiment-Analysis-Dataset.zip"
	unzip "Sentiment-Analysis-Dataset.zip"
	rm "Sentiment-Analysis-Dataset.zip"
	mv "Sentiment Analysis Dataset.csv" "source.csv"

tag-upload:
	docker tag vsu-sentiment:prod igrishaev/vsu:sentiment
	docker push igrishaev/vsu:sentiment
