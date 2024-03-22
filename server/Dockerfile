FROM python:3.9

# upgrade pip
RUN pip install --upgrade pip
RUN pip install --default-timeout=100 future

COPY requirements.txt ./
COPY *.py ./

# # install requirements
RUN pip install -r ./requirements.txt

# command to run server
CMD ["python", "adaptor.py"]