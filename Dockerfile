FROM python:3.11.3-alpine3.18

ENV PYTHONUNBUFFERED 1
ENV PATH="/scripts:${PATH}"

COPY ./requirements.txt /requirements.txt
RUN apk add --update --no-cache --virtual .tmp gcc libc-dev linux-headers
RUN pip install -r /requirements.txt
RUN apk del .tmp

RUN mkdir /app
COPY ./myagilos_proposal /app
WORKDIR /app

COPY ./scripts /scripts
RUN chmod +x /scripts/*

RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static


RUN adduser -D user
RUN chown -R user:user /vol
RUN chown -R user:user /app
RUN chown user:user /app/db.sqlite3  # Set ownership for the database file
RUN chmod -R 755 /vol/web
RUN chmod -R 755 /app
RUN chmod 664 /app//db.sqlite3  # Set permissions for the database file

USER user
CMD ["entrypoint.sh"]