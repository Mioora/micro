FROM python:3.10

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

COPY ./entry.sh /code/entry.sh

RUN chmod +x /code/entry.sh

CMD ["/code/entry.sh"]