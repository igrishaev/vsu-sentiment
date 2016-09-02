FROM python:2

ENV PYTHONDONTWRITEBYTECODE 1
ENV FLASK_DEBUG 1

COPY pip.requirements* /app/
WORKDIR /app
RUN pip install -r pip.requirements.txt
RUN rm pip.requirements*

CMD ["uwsgi", "uwsgi.ini"]
