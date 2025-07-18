# Dockerfile
FROM prefecthq/prefect:2-python3.10

# Set working directory
WORKDIR /opt/flows

RUN apt-get update && apt-get install -y curl

# Install Evidently explicitly and print output for verification
RUN pip install --no-cache-dir evidently && \
    python -c "from evidently import Report"
