FROM python:3-slim

RUN apt-get update \
    && apt-get install git -y \
    && rm -rf /var/lib/apt/lists/*
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