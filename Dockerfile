FROM alpine:latest
MAINTAINER Raul Perez <repejota@gmail.com>

ADD requirements.txt /tmp/requirements.txt

RUN apk update && \
  apk upgrade && \
  apk add --no-cache python3 py3-psycopg2 git && \
  pip3 install -r /tmp/requirements.txt && \
  rm -rf /var/cache/apk/*

ADD . /opt/vtalks.net
WORKDIR /opt/vtalks.net/web

CMD ["./start.sh"]