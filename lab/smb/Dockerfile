FROM debian:bookworm-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    samba \
    && rm -rf /var/lib/apt/lists/*

# Cria usuário de sistema e registra sua senha no banco do Samba (smbpasswd)
RUN useradd -m -s /usr/sbin/nologin samba \
    && (echo "pass123"; echo "pass123") | smbpasswd -s -a samba

RUN mkdir -p /srv/samba/labs && chown -R samba:samba /srv/samba/labs

COPY smb.conf /etc/samba/smb.conf

EXPOSE 139 445

CMD ["smbd", "--foreground", "--no-process-group", "--debug-stdout"]
