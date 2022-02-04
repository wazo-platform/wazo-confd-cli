FROM python:3.7-slim-buster AS compile-image
LABEL maintainer="Wazo Maintainers <dev@wazo.community>"

RUN python -m venv /opt/venv
# Activate virtual env
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt /usr/src/wazo-confd-cli/
WORKDIR /usr/src/wazo-confd-cli
RUN pip install -r requirements.txt

COPY setup.py /usr/src/wazo-confd-cli/
COPY wazo_confd_cli /usr/src/wazo-confd-cli/wazo_confd_cli
RUN python setup.py install

FROM python:3.7-slim-buster AS build-image
COPY --from=compile-image /opt/venv /opt/venv

COPY ./etc/wazo-confd-cli /etc/wazo-confd-cli
RUN true \
    && mkdir -p /etc/wazo-confd-cli/conf.d \
    # create empty config dir to avoid override system config
    && mkdir -p /root/.config/wazo-confd-cli

# Activate virtual env
ENV PATH="/opt/venv/bin:$PATH"
ENTRYPOINT ["wazo-confd-cli"]
