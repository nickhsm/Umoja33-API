
FROM python:3.11-slim

WORKDIR /app


COPY . .
RUN pip install -r requirements.txt --no-cache-dir
RUN PYTHONPATH=. python src/database/database_connection.py



ENTRYPOINT fastapi run

