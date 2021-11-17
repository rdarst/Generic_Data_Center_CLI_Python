FROM alpine:3.14.3
RUN apk update && \ 
    apk add --no-cache python3 && \
    apk upgrade 
COPY gdc.py /
