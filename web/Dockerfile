FROM alpine:latest
MAINTAINER Raul Perez <repejota@gmail.com>

RUN apk add --no-cache --update bash python3 python3-dev py-tz ca-certificates postgresql-dev gcc g++

WORKDIR /opt/vtalks/web
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY start.sh .

CMD ["./start.sh"]
