FROM public.ecr.aws/docker/library/alpine:3.14

RUN apk add py3-pip \
    && pip install --upgrade pip

ENV DATABASE_URI=postgresql://postgres:postgres@my-blacklist-db.cy9comua4vhw.us-east-1.rds.amazonaws.com:5432/blacklist_db
ENV DB_HOST=my-blacklist-db.cy9comua4vhw.us-east-1.rds.amazonaws.com
ENV DB_NAME=blacklist_db
ENV DB_PASS=postgres
ENV DB_PORT=5432
ENV DB_USER=postgres
ENV FLASK_DEBUG=true
ENV JWT_SECRET_KEY=clave-secreta
ENV PYTHONPATH=/var/app/venv/staging-LQM1lest/bin


WORKDIR /app
COPY . /app/

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python3", "application.py"]

RUN pip install newrelic
ENV NEW_RELIC_APP_NAME="blacklists"
ENV NEW_RELIC_LOG=stdout
ENV NEW_RELIC_DISTRIBUTED_TRACING_ENABLED=true
#INGEST_License
ENV NEW_RELIC_LICENSE_KEY=acc696385838ea6734fd73c941bd6537FFFFNRAL
ENV NEW_RELIC_LOG_LEVEL=info

ENTRYPOINT ["newrelic-admin", "run-program"]