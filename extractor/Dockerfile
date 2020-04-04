FROM python:3.6.10-buster

ENV PG_DATABASE=
ENV PG_USERNAME=
ENV PG_PASSWORD=
ENV PG_HOST=
ENV PG_PORT=
ENV DAYS=

COPY . /app
ADD https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh /app/wait-for-it.sh

RUN pip install -r /app/requirements.txt

CMD /app/wait-for-it.sh $PG_HOST:$PG_PORT --strict -- python /app/main.py --database $PG_DATABASE --user $PG_USERNAME --password $PG_PASSWORD --host $PG_HOST --port $PG_PORT --days $DAYS