FROM python:2

ENV PYTHONDONTWRITEBYTECODE 1
ENV FLASK_DEBUG 1

EXPOSE 8080 9191

COPY pip.requirements* /app/
WORKDIR /app
RUN pip install -r pip.requirements.txt
RUN rm pip.requirements*

COPY . /app/
RUN python src/sentiment.py

CMD ["uwsgi", "uwsgi.ini"]
