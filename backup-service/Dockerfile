FROM alpine:latest

RUN apk add --no-cache \
    mongodb-tools \
    curl \
    tar \
    gzip \
    bash

COPY backup.sh /backup.sh
COPY restore.sh /restore.sh
RUN chmod +x /backup.sh /restore.sh

CMD ["/backup.sh"]
