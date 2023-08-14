#################################################################################
# STAGE - BUILD
#################################################################################
# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.10.11-slim-buster as builder
EXPOSE 8000
# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1
# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1
# Install pip requirements
COPY requirements.txt .
RUN python -m pip install --no-cache-dir --disable-pip-version-check -r requirements.txt
WORKDIR /app
COPY . /app

#################################################################################
# STAGE - TESTS
#################################################################################
FROM builder as tests
RUN python -m pip install --no-cache-dir --disable-pip-version-check -r requirements-dev.txt

#################################################################################
# STAGE - RUNTIME
#################################################################################
FROM python:3.10.11-slim-buster AS runtime
WORKDIR /app
COPY --from=builder /app /app
# TODO: it should be possible to copy the installed packages but instead we reinstall
#COPY --from=builder /usr/local/lib/python3.10/ /usr/local/lib/python3.10/
RUN python -m pip install --no-cache-dir --disable-pip-version-check -r requirements.txt

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD uvicorn pyhgvs.api:app --host 0.0.0.0 --port 8000 --timeout-graceful-shutdown 10