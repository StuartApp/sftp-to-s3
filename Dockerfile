FROM python:3-alpine
COPY run.py /app/
COPY src /app/src

WORKDIR /app
RUN apk add py3-boto3 py3-paramiko py3-yaml

ENV PYTHONPATH="/usr/lib/python3.8/site-packages"
EXPOSE 3373
ENTRYPOINT ["/app/run.py"]
