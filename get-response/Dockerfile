FROM python:3.11-slim as base
# Setup env
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1

RUN apt-get update && apt-get install -y --no-install-recommends gcc && apt-get install build-essential -y

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY get.py .
EXPOSE 8000
CMD [ "python", "-m" , "uvicorn", "get:app", "--host", "0.0.0.0", "--port", "8000"]