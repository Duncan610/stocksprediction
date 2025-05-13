# FROM python:alpine
FROM python:3.13-slim
WORKDIR /app
RUN apt-get update && apt-get upgrade -y && apt-get clean && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt apache-airflow==2.9.0
COPY src/ src/
COPY airflow/dags/ airflow/dags/
ENV PYTHONPATH=/app
ENV AIRFLOW_HOME=/app/airflow
CMD ["airflow", "scheduler"]