FROM alpine:3.14.3
RUN apk update && \ 
    apk del ncurses ncurses-libs && \ 
    apk add ncurses ncurses-libs --repository=http://dl-cdn.alpinelinux.org/alpine/edge/main && \
    apk upgrade busybox --repository=http://dl-cdn.alpinelinux.org/alpine/edge/main && \
    apk add --no-cache python3 && \
    apk upgrade 
COPY gdc.py /
