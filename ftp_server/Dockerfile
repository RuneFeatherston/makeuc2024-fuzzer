# ftp_server/Dockerfile
FROM debian:slim

RUN apt-get update && apt-get install -y \
    vsftpd && \
    rm -rf /var/lib/apt/lists/*

COPY vsftpd.conf /etc/vsftpd.conf

# Expose FTP port 21
EXPOSE 21

CMD ["vsftpd", "/etc/vsftpd.conf"]
