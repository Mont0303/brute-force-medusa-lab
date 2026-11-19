FROM debian:bookworm-slim

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    proftpd-core \
    && rm -rf /var/lib/apt/lists/*

# Cria usuário de laboratório com credencial fraca presente nas wordlists
RUN useradd -m -s /bin/bash msfadmin && echo "msfadmin:msfadmin" | chpasswd

EXPOSE 21

CMD ["proftpd", "-n"]
