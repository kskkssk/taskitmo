FROM python:3.11-slim
RUN apt-get update && apt-get install -y git
RUN pip install dvc

WORKDIR /app

COPY app/requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY app /app

EXPOSE 8080
CMD ["python", "api.py"]