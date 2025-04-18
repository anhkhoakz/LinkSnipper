FROM python:3.14-rc-slim-bookworm@sha256:a4722702deceb57f9e99a23582857a7723598c6e2998dfa6e768d8ca9da53e77

LABEL maintainer="anhkhoakz"
LABEL version="0.0.1"

# Set the working directory
WORKDIR /app

RUN pip install uv

COPY pyproject.toml .
COPY . .

RUN uv sync

# Define the command to run the application
CMD ["uv", "run", "python", "main.py"]
