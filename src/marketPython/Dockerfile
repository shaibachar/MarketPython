FROM python:3.6.3
ADD . /marketPython
WORKDIR /marketPython
RUN pip install -r requirements.txt
CMD ["gunicorn", "-w 4", "main:app"]