# set base image (host OS)
FROM python:3.7

# set the working directory in the container
WORKDIR /code

# copy the dependencies file to the working directory
COPY requirements.txt .

# install dependencies
RUN pip install -r requirements.txt

# copy the content of the local src directory to the working directory
COPY src/ .

EXPOSE 8092
# command to run on container start
CMD [ "opentelemetry-instrument", "python", "./server.py" ]