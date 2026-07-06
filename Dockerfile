FROM python:3.11-slim

WORKDIR /app

# Copy project configuration and sources
COPY pyproject.toml LICENSE README.md ./
COPY src/ ./src/

# Install hatchling (build backend) and dependencies, then the app itself
RUN pip install --no-cache-dir hatchling
RUN pip install --no-cache-dir . uvicorn starlette sse-starlette

# Expose port for health checks and Streamable HTTP transport
EXPOSE 8000

# Run Streamable HTTP at /mcp by default on Kakao Cloud
CMD ["python", "-m", "idea_box_mcp.server", "streamable-http"]
