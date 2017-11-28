FROM alpine:latest
MAINTAINER Raul Perez <repejota@gmail.com>

RUN apk add --no-cache python3 python3-dev py-tz ca-certificates postgresql-dev gcc g++

RUN mkdir -p /opt/vtalks/web
ADD requirements.txt /opt/vtalks/web
ADD start.sh /opt/vtalks/web
WORKDIR /opt/vtalks/web
RUN pip3 install -r requirements.txt

CMD ["./start.sh"]
