FROM alpine:latest
MAINTAINER Raul Perez <repejota@gmail.com>

RUN apk add --no-cache python3 python3-dev py-tz ca-certificates \
    postgresql-dev gcc g++
RUN mkdir -p /opt/vtalks/web
WORKDIR /opt/vtalks/web

ADD . /opt/vtalks/web
RUN pip3 install -r requirements.txt

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
