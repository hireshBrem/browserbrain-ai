FROM python:3.12-slim

WORKDIR /app

# Install uv tooling
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
COPY --from=ghcr.io/astral-sh/uv:latest /uvx /usr/local/bin/uvx

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv venv && uv sync --frozen

# Pre-install Playwright browser to satisfy browser-use requirements
RUN uvx playwright install --with-deps chromium

# Copy application code
COPY . .

# Expose port 4000
EXPOSE 4000

# Run the FastAPI server using uvicorn
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "4000", "--reload"]

