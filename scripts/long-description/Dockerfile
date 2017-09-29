FROM python:3

WORKDIR /usr/src/long-description
 
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./long_description.py .

CMD [ "python", "./long_description.py" ]

