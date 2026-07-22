# Chapter 16 -- Deployment and Production
# Generic Dockerfile for a FastAPI agent app (Section 16.3, "Dockerizing").
# Build:  docker build -t my-agent .
# Run:    docker run -p 8000:8000 -e OPENAI_API_KEY=$OPENAI_API_KEY my-agent
# NOTE: never bake API keys into the image; pass them at run time with -e
# or a secrets manager.

FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
