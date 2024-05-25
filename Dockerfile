FROM python:slim

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.5.0

RUN mkdir /home/lhcpiv
WORKDIR /home/lhcpiv/

COPY . .

RUN apt-get update
RUN apt-get install htop ffmpeg libsm6 libxext6 libgl1-mesa-glx python3-opencv -y
RUN apt-get update && \
    apt-get install --no-install-recommends htop=2.2.0 ffmpeg=7:4.3.1-0+deb11u1 libsm6=2:1.2.3-1 libxext6=2:1.3.4-0ubuntu1 libgl1-mesa-glx=20.2.6-0ubuntu0.20.04.1 python3-opencv=4.2.0.34-1 -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    PYTHONDONTWRITEBYTECODE=1 pip install --no-cache-dir -r requirements.lock

CMD ["jupyter", "lab", "--port", "8888", "--ip", "0.0.0.0", "--allow-root", "--no-browser"]
