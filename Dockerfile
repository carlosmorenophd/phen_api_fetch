FROM python:3.10-bookworm
WORKDIR /app
COPY ./requirements.txt /requirements.txt
RUN pip install --no-cache-dir --upgrade -r /requirements.txt

COPY app/ .

CMD ["python", "main.py"]