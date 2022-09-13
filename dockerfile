FROM python:3

COPY scripts/*.py /src/
COPY requirements.txt /src/

RUN pip install -r /src/requirements.txt

