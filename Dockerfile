FROM python:3.9-slim
WORKDIR /app
RUN apt-get update && apt-get upgrade -y && apt-get clean && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt
COPY src/ src/
COPY airflow/dags/ airflow/dags/
ENV PYTHONPATH=/app
ENV AIRFLOW_HOME=/app/airflow
CMD ["airflow", "scheduler"]