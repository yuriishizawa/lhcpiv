FROM python:3.11

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.5.0

# Instalação do poetry versão 1.5.0
RUN pip3 install "poetry==$POETRY_VERSION"

RUN mkdir /home/lhcpiv
WORKDIR /home/lhcpiv/

COPY . .

RUN apt-get update
RUN apt-get install htop ffmpeg libsm6 libxext6 libgl1-mesa-glx python3-opencv -y
RUN poetry install

CMD ["jupyter", "lab", "--port", "8888", "--ip", "0.0.0.0", "--allow-root", "--no-browser"]
