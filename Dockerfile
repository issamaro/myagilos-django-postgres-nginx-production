FROM python:3.11.3-alpine3.18

ENV PYTHONUNBUFFERED 1
ENV PATH="/scripts:${PATH}"
ENV PATH="/usr/lib/postgresql/X.Y/bin/:${PATH}"

COPY ./requirements.txt /requirements.txt
RUN apk add --update --no-cache --virtual .tmp gcc libc-dev linux-headers && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-deps \
        build-base postgresql15-dev musl-dev \
        libpq-dev python3-dev libffi-dev && \
    pip install -r /requirements.txt && \
    apk del .tmp-deps && \
    apk del .tmp

RUN mkdir /app
COPY ./myagilos_proposal /app
WORKDIR /app

COPY ./scripts /scripts
RUN chmod +x /scripts/*

RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static


RUN adduser -D user
RUN chown -R user:user /vol && \
    chown -R user:user /app
# RUN chown user:user /app/db.sqlite3
RUN chmod -R 755 /vol/web && \
    chmod -R 755 /app
# RUN chmod 664 /app/db.sqlite3

USER user
CMD ["entrypoint.sh"]