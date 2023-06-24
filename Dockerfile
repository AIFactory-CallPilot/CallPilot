FROM public.ecr.aws/lambda/python:3.10

COPY requirements.txt ${LAMBDA_TASK_ROOT}

COPY ffmpeg /usr/local/bin/ffmpeg
RUN chmod 777 -R /usr/local/bin/ffmpeg

RUN pip install -r requirements.txt

COPY app.py ${LAMBDA_TASK_ROOT}
COPY asdf.mp3 ${LAMBDA_TASK_ROOT}
COPY speech_to_text.py ${LAMBDA_TASK_ROOT}

CMD [ "app.handler" ]

## Define global args
#ARG FUNCTION_DIR="/home/app/"
#ARG RUNTIME_VERSION="3.9"
#
## Stage 1 - bundle base image + runtime
## Grab a fresh copy of the image and install GCC
#FROM python:${RUNTIME_VERSION}-alpine AS python-alpine
## Install GCC (Alpine uses musl but we compile and link dependencies with GCC)
#RUN apk add --no-cache \
#    libstdc++
#
## Stage 2 - build function and dependencies
#FROM python-alpine AS build-image
## Install aws-lambda-cpp build dependencies
#RUN apk add --no-cache \
#    build-base \
#    libtool \
#    autoconf \
#    automake \
#    make \
#    cmake \
#    libcurl \
#    ffmpeg
## Include global args in this stage of the build
#ARG FUNCTION_DIR
#ARG RUNTIME_VERSION
## Create function directory
#RUN mkdir -p ${FUNCTION_DIR}
#WORKDIR .
## Copy handler function
#COPY . ${FUNCTION_DIR}
#WORKDIR ${FUNCTION_DIR}
## Optional – Install the function's dependencies
#RUN python3 -m pip install -r requirements.txt --target ${FUNCTION_DIR}
## Install Lambda Runtime Interface Client for Python
#RUN python3 -m pip install awslambdaric --target ${FUNCTION_DIR}
#
## Stage 3 - final runtime image
## Grab a fresh copy of the Python image
#FROM python-alpine
## Include global arg in this stage of the build
#ARG FUNCTION_DIR
## Set working directory to function root directory
#WORKDIR ${FUNCTION_DIR}
## Copy in the built dependencies
#COPY --from=build-image ${FUNCTION_DIR} ${FUNCTION_DIR}
## (Optional) Add Lambda Runtime Interface Emulator and use a script in the ENTRYPOINT for simpler local runs
#ADD https://github.com/aws/aws-lambda-runtime-interface-emulator/releases/latest/download/aws-lambda-rie /usr/bin/aws-lambda-rie
#COPY entry.sh /
#RUN chmod 755 /usr/bin/aws-lambda-rie /entry.sh
#ENTRYPOINT [ "/entry.sh" ]
#CMD [ "app.handler" ]