# DESCRIPTIONS: Minimal container image for the tiny agent (no secrets baked in)
FROM python:3.12-slim

# DESCRIPTIONS: Create workdir and install deps
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# DESCRIPTIONS: Add agent code; do NOT copy .env into image
COPY agent.py .

# DESCRIPTIONS: Default command
CMD ["python", "agent.py"]
