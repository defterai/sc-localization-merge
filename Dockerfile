FROM debian:stable-slim

LABEL "maintainer"="Defter"
LABEL "repository"="https://github.com/defterai/sc-localization-merge"
LABEL "version"="0.1.0"

COPY localization.py /localization.py
COPY xlsx_to_ini_with_ref.py /xlsx_to_ini_with_ref.py
COPY entrypoint.sh /entrypoint.sh

RUN apt-get update; \
    apt-get install -y python3 python3-pip; \
    apt-get clean -y; \
    rm -rf /var/lib/apt/lists/*; \
    chmod +x /entrypoint.sh; \
    python3 -m pip install pandas; \
    python3 -m pip install xlrd

ENTRYPOINT ["/entrypoint.sh"]