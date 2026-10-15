FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
RUN groupadd -r pmk && useradd -r -g pmk -d /app pmk
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN mkdir -p /app/media /app/staticfiles && chown -R pmk:pmk /app
USER pmk
EXPOSE 8000
CMD ["gunicorn","config.wsgi:application","--bind","0.0.0.0:8000","--workers","3","--access-logfile","-"]
