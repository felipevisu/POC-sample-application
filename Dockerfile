FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt requirements-dev.txt ./

RUN pip install --no-cache-dir -r requirements.txt \
 && pip install --no-cache-dir -r requirements-dev.txt

COPY . .

# Default command for running the app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
