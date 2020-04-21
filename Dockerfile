FROM python:3.7-slim

WORKDIR /src

RUN apt-get update \
	&& apt-get -y install git procps \
	&& git clone https://github.com/emericg/OpenSubtitlesDownload.git
