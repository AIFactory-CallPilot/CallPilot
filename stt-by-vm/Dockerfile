FROM python:3.11-slim as base
# Setup env
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1

RUN apt-get update && apt-get install -y --no-install-recommends gcc && apt-get install git -y

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY ffmpeg /usr/local/bin/ffmpeg
COPY small.pt .
RUN chmod 777 -R /usr/local/bin/ffmpeg

COPY speech_to_text.py .

CMD [ "python", "speech_to_text.py"]
