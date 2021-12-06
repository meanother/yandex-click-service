FROM alpine:latest

RUN apk update && apk add tor obfs4proxy

COPY torrc /etc/tor/torrc
RUN chown -R tor /etc/tor

USER tor

ENTRYPOINT ["tor"]

CMD ["-f", "/etc/tor/torrc"]