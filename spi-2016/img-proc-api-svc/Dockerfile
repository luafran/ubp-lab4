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
EXPOSE 8082

# Wait for mysql and rabbitmq and run the application
CMD sleep 5 && python /usr/src/app/img-proc-api-svc/application.py
