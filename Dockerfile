FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10

RUN pip3 install pipenv

# -- Adding Pipfiles
COPY ./src/Pipfile Pipfile
COPY ./src/Pipfile.lock Pipfile.lock

# -- Install dependencies:
RUN pipenv install

COPY ./src /app