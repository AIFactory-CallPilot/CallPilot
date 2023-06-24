FROM amazonlinux

# init
RUN yum update -y
# install python3 on OS
RUN yum install python3 python3-pip zip wget tar xz -y

# install virtualenv
RUN pip3 install --user virtualenv
# make venv and dist dirs
RUN mkdir /home/venv
RUN mkdir -p /home/dist/python
# copy entrypoint.sh
COPY ./deploy/entrypoint.sh entrypoint.sh
COPY ./requirements.txt requirements.txt
RUN chmod +x entrypoint.sh