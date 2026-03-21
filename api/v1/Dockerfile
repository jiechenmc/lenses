FROM python:3.9-slim

# Install build tools
RUN apt-get update && apt-get install -y curl unzip ca-certificates

RUN curl -Ls https://astral.sh/uv/install.sh | sh && \
    cp $HOME/.local/bin/uv /usr/local/bin/uv

WORKDIR /code

# Copy pyproject.toml and uv.lock
COPY pyproject.toml uv.lock /code/

# Install packages with uv
RUN uv sync
RUN ln -s /code/.venv/bin/uvicorn /usr/local/bin/uvicorn

# Copy app code
COPY . /code

# Activate the environment and run your app

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]

