FROM fedora:latest

RUN dnf -y update && dnf clean all && \
dnf -y install openssl-devel python3-devel \
rpm-devel krb5-devel make gcc findutils which git && \
dnf clean all

RUN groupadd -r -g 2000 koji; useradd koji --uid 2000 --gid 2000

USER koji
