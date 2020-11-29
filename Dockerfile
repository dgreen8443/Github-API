FROM python:3

WORKDIR /usr/src/github-api


#RUN pip install --no-cache-dir -r requirements.txt

COPY ./Access.py .

CMD [ "python", "./Access.py" ]