FROM python:3.13-slim

WORKDIR /marketsimulator

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN pip install --no-cache-dir .

# Run the application
CMD ["python", "-m", "marketsimulator"]
