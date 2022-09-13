FROM python:3

COPY scripts/*.py /src/
COPY requirements.txt /src/

RUN --mount=type=secret,id=my_env source /run/secrets/my_env \
  && pip install -r /src/requirements.txt

CMD [ "python", "src/app.py" ]