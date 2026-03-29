FROM python:3.9-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir flask requests beautifulsoup4 schedule

EXPOSE 15554

CMD ["python", "app.py"]