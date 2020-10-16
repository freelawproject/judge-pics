FROM python:3.8-slim

#Copy project to Docker image
COPY . /project/
WORKDIR /project

#Install requirements
RUN pip install -r requirements.txt

# Install judge-pics
RUN python setup.py install

