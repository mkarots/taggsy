FROM python:3.7


COPY ./taggy/requirements.txt /
RUN pip install -r /requirements.txt

COPY ./taggy/taggy /app/taggy
COPY ./taggy/tests /app/tests

WORKDIR /app

CMD ["nosetests", "tests"]

