FROM python:3.10.12

LABEL MAINTAINER="Alan STEPHAN"

WORKDIR /workdir
SHELL ["/bin/bash", "-c"]

ARG user=appuser
ARG group=appuser
ARG uid=1000
ARG gid=1000

RUN apt-get update -y && apt-get upgrade -y

RUN groupadd -g ${gid} ${group} && useradd -u ${uid} -g ${group} -m -s /bin/sh ${user} 


COPY ./app /workdir/app
COPY ./requirements.txt /workdir/requirements.txt
COPY ./run.py /workdir/run.py

RUN chown -R ${user}:${group} /workdir

USER ${uid}:${gid}

RUN pip install --upgrade pip --no-warn-script-location && pip install -r requirements.txt --no-warn-script-location && rm requirements.txt
ENV PATH="$PATH:/home/${user}/.local/bin"

RUN opentelemetry-bootstrap -a install

CMD ["python3","run.py"]