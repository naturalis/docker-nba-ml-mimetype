FROM python:3-alpine

ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt
ADD generate_mimetype.py generate_mimetype.py

CMD [ "python", "./generate_mimetype.py" ]
