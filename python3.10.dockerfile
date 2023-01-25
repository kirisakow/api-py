FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10

COPY ./requirements.txt /app/
COPY ./whatever_disentangler /app/whatever_disentangler

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./assets /app/assets
COPY ./main.py /app