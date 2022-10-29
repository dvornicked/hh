FROM python:3.9-slim
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /opt/app
COPY poetry.lock pyproject.toml ./
RUN pip3 install poetry
RUN apt-get update && apt-get install -y libpq-dev gcc
RUN poetry install
RUN apt-get autoremove -y gcc
COPY . .
EXPOSE 8000