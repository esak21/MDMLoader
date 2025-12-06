# ==========================================
# Stage 1: Builder
# ==========================================
# EXPLICITLY use bookworm (Debian 12) to ensure OpenJDK 17 is available
FROM python:3.11-slim-bookworm AS builder

# Install uv directly from the official image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Set working directory
WORKDIR /app

# Environment variables to optimize uv behavior
# UV_COMPILE_BYTECODE: Compiles Python source files to bytecode for faster startup
# UV_LINK_MODE: Copies files instead of hardlinking (safer for Docker layer caching)
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK MODE=copy

# 1. Copy configuration files first (for layer caching)
COPY pyproject.toml uv.lock ./

# 2. Install dependencies
# --frozen: Ensure the lockfile is respected exactly
# --no-install-project: Only install dependencies (pyspark, etc.) first
# --no-dev: Exclude development dependencies (pytest, etc.)
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev

# 3. Copy the rest of the application code
COPY . .

# 4. Install the project itself
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# ==========================================
# Stage 2: Runtime (Final Image)
# ==========================================
# EXPLICITLY use bookworm (Debian 12)
FROM python:3.11-slim-bookworm

WORKDIR /app


# Copy the virtual environment from the builder stage
COPY --from=builder /app/.venv /app/.venv

# Copy the application source code
COPY data/ ./data/

# Copy the application source code
COPY src/ ./src/

# Add the virtual environment binaries to the PATH
ENV PATH="/app/.venv/bin:$PATH"

# Entry point
CMD ["python", "src/runner.py" , "gym_membership.csv"]