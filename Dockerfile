FROM python:3

ADD requirements.txt /app/
RUN pip install -r /app/requirements.txt 

ADD supervisor.py /app/

WORKDIR /app
ARG NS="default"
CMD kopf run --namespace=${NS} supervisor.py