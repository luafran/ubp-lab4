FROM alpine:latest

# Install python and pip
RUN apk add --update py-pip

# upgrade pip
RUN pip install --upgrade pip

# install Python modules needed by the Python app
ADD . /usr/src/app
WORKDIR /usr/src/app
RUN pip install --no-cache-dir -r requirements.txt

# tell the port number the container should expose
EXPOSE 8083

# run the application
CMD ["python", "/usr/src/app/storage-svc/application.py"]
