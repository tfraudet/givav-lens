FROM python:3.14.2-alpine3.23

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install python deps first (cached if requirements unchanged)
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy application sources
COPY . /app

# Create a non-root user and give ownership of the app dir
RUN adduser -D appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8501
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "main.py"]
