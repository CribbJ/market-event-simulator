FROM python:3.13-slim

WORKDIR /marketsimulator

COPY pyproject.toml .
RUN pip install --no-cache-dir .

COPY . .

# Run the application
CMD ["python", "-m", "marketsimulator"]
