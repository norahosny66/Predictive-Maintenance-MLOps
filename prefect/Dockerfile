# Use Prefect base image with Python 3.10
FROM prefecthq/prefect:2-python3.10

# Set the working directory for Prefect
WORKDIR /opt/flows

# Cache APT and pip to avoid reinstalling on every build
RUN --mount=type=cache,target=/var/cache/apt \
    --mount=type=cache,target=/root/.cache/pip \
    apt-get update && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/* \
    && pip install evidently \
    && python -c "from evidently import Report"


# Copy your project into the image (so it can be installed)
# Even though we'll also mount it for development, this ensures
# the package is installed for Prefect deployments and remote agents.
COPY . /opt/flows/predictive_maintenance_project

# Set working directory to the project root
WORKDIR /opt/flows/predictive_maintenance_project

# Install the project as a package (editable for dev)
RUN pip install --no-cache-dir -e .

ENV PYTHONPATH="/opt/flows/predictive_maintenance_project/src:${PYTHONPATH}"

# Default back to /opt/flows for Prefect commands
WORKDIR /opt/flows
