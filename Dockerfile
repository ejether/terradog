FROM python:3-slim

RUN apt-get update \
    && apt-get install git curl unzip -y \
    && rm -rf /var/lib/apt/lists/*
RUN curl -o terraform.zip https://releases.hashicorp.com/terraform/0.14.3/terraform_0.14.3_linux_amd64.zip \
    && unzip terraform.zip && mv terraform /usr/local/bin/ && chmod +x /usr/local/bin/terraform

RUN useradd -m terradoguser

RUN chown -R terradoguser:terradoguser /home/terradoguser

USER terradoguser
WORKDIR /home/terradoguser

ENV HOME=/home/terradoguser/
ENV PATH="$PATH:/home/terradoguser/.local/bin"

ADD . /home/terradoguser/terradog
RUN python -m pip install ./terradog --no-cache-dir --user

ENTRYPOINT ["terradog"]
CMD ["--version"]
