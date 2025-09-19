FROM python:3.11-slim

RUN pip install psycopg[binary]

WORKDIR /app
COPY sdl_laba_2.py .

CMD ["python", "sdl_laba_2.py"]
