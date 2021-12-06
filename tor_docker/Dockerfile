FROM alpine:latest

RUN apk update && apk add tor go git ca-certificates \
    && mkdir -p /go/src /go/bin \
    && chmod -R 644 /go

ENV GOPATH /go
ENV PATH /go/bin:$PATH

run git clone https://gitlab.com/yawning/obfs4.git \
    && cd obfs4 \
    && go build -o obfs4proxy ./obfs4proxy \
    && mv obfs4proxy/obfs4proxy /usr/bin/obfs4proxy

COPY torrc /etc/tor/torrc
RUN chown -R tor /etc/tor

USER tor

ENTRYPOINT ["tor"]

CMD ["-f", "/etc/tor/torrc"]