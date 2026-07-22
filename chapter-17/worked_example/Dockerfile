# Chapter 16 -- Deployment and Production
# Worked Example: Dockerising a 2-Tool Agent (Section 16.9).
# Build:  docker build -t two-tool-agent .
# Run:    docker run -p 8000:8000 -e OPENAI_API_KEY=$KEY two-tool-agent
# Test:   curl -X POST localhost:8000/ask \
#              -H "Content-Type: application/json" \
#              -d '{"q": "What is 13*19?"}'

FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
