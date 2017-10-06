FROM python:3

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /usr/src/long-description

RUN ["chmod", "o+w", "."]

USER nobody:nogroup

COPY ./long_description.py .

CMD [ "python", "./long_description.py" ]

