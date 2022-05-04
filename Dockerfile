FROM registry.access.redhat.com/ubi8/ubi:latest

ENV HOME=/insights-results-aggregator-utils \
    REQUESTS_CA_BUNDLE="/etc/pki/tls/certs/ca-bundle.crt"

WORKDIR $HOME

COPY . .

RUN dnf -y --setopt=tsflags=nodocs install zlib python3.8 git wget gcc make python3-devel && \
    wget https://password.corp.redhat.com/RH-IT-Root-CA.crt && \
    cp RH-IT-Root-CA.crt /etc/pki/ca-trust/source/anchors/RH-IT-Root-CA.crt && \
    update-ca-trust

RUN python3 -m pip install --upgrade pip && \
    pip3 install .

USER 1001