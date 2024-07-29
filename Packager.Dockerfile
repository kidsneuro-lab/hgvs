FROM python:3.10-slim
ARG VERSION=0.1.0

# Argument for version number
WORKDIR /app
COPY . /app

# Update the backage build version
RUN pip install build toml
RUN echo "Updating version in pyproject.toml to ${VERSION}..."
RUN python /app/pyproject_update.py $VERSION
RUN cat pyproject.toml
RUN pip install -r requirements.txt

# Set the entrypoint to run the build process
ENTRYPOINT ["python", "-m", "build"]