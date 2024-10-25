FROM python:3.9

RUN pip install requests
WORKDIR /app
COPY smoketest.py smoketest.py
CMD ["python", "smoketest.py"]
