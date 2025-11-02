FROM python:3.12-slim

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv venv && uv sync --frozen

# Copy application code
COPY . .

ARG BROWSER_USE_API_KEY

# Set environment variable for Browser Use API Key (can be overridden at runtime)
ENV BROWSER_USE_API_KEY=$BROWSER_USE_API_KEY

# Expose port 4000
EXPOSE 4000

# Run the FastAPI server using uvicorn
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "4000", "--reload"]

