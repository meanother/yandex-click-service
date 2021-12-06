FROM alpine:latest

RUN apk update && apk add tor go git ca-certificates \
    && mkdir -p /go/src /go/bin \
    && chmod -R 644 /go

ENV GOPATH /go
ENV PATH /go/bin:$PATH

RUN go get git.torproject.org/pluggable-transports/obfs4.git/obfs4proxy \
    && mv /go/bin/obfs4proxy /usr/bin/obfs4proxy

COPY torrc /etc/tor/torrc
RUN chown -R tor /etc/tor

USER tor

ENTRYPOINT ["tor"]

CMD ["-f", "/etc/tor/torrc"]