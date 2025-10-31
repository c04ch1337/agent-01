# DESCRIPTIONS: Minimal container for the tiny agent
FROM python:3.12-slim

# DESCRIPTIONS: App workspace
WORKDIR /app

# DESCRIPTIONS: Install the only dependency (requests) without cache
RUN pip install --no-cache-dir requests

# DESCRIPTIONS: Add agent code and set default command
COPY agent.py .
CMD ["python", "agent.py"]
