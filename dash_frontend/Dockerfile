# pull official base image
FROM python:3.11.6-slim

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV POETRY_VERSION=1.7.1
#ENV PYTHONPATH="${PYTHONPATH}:/my/other/path"


# install dependencies
RUN apt-get update \
    && apt-get -y install libpq-dev gcc

RUN pip install --upgrade pip

RUN pip install "poetry==$POETRY_VERSION"

COPY poetry.lock pyproject.toml /usr/src/app/

RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

# copy project
COPY . /usr/src/app/dash_frontend

#RUN chmod +x models_billing/entrypoint.sh

#ENTRYPOINT ["models_billing/entrypoint.sh"]

CMD ["sh", "-c", "python -m dash_frontend.app"]
