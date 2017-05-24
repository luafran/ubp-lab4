FROM alpine:latest

# Install python and pip
RUN apk add --update build-base openssl-dev python-dev py-pip

# upgrade pip
RUN pip install --upgrade pip

# install Python modules needed by the Python app
ADD . /usr/src/app
WORKDIR /usr/src/app
RUN pip install --no-cache-dir -r requirements.txt

# tell the port number the container should expose
EXPOSE 8081

# Wait for mysql and run the application
CMD sleep 5 && python /usr/src/app/auth-svc/auth-svc.py
