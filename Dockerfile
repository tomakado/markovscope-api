FROM python:3.8.5
WORKDIR /app/

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app app
COPY data data
COPY run.py .
COPY docker-entrypoint.sh .

RUN chmod +x docker-entrypoint.sh

EXPOSE 8000

CMD ["./docker-entrypoint.sh"]