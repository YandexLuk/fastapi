FROM python:3.13.13-alpine

ENV PATH="${PATH}:/root/.local/bin"
COPY ./fastapi_app/src /app/src
COPY migrations /app/migrations
COPY alembic.ini /app/
COPY requirements.txt /app/

ENV PYTHONPATH /app/src
WORKDIR /app
RUN pip install -r ./requirements.txt
RUN chmod +x ./src/start.sh
EXPOSE 8000
