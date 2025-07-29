FROM python:3.9

WORKDIR /app

COPY example-python-container/requirements.txt .
RUN pip install -r requirements.txt

COPY example-python-container/ .

CMD ["python", "workload_identity.py"]
