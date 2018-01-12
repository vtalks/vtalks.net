FROM alpine:latest
MAINTAINER Raul Perez <repejota@gmail.com>

ADD . /opt/vtalks/web
WORKDIR /opt/vtalks/web

RUN apk update && \
  apk upgrade && \
  apk add --no-cache python3 py3-psycopg2 git && \
  pip3 install -r requirements.txt && \
  rm -rf /var/cache/apk/*

CMD ["./start.sh"]
