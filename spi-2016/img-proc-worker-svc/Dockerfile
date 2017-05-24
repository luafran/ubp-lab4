FROM java:openjdk-8-jre-alpine

RUN apk add --no-cache curl wget ca-certificates bash

ADD build/libs/img-proc-worker-svc-0.0.1-dev.jar /opt/worker-svc/worker-svc-0.0.1-dev.jar

# Wait for rabbitmq and run the application
CMD sleep 5 && java -jar /opt/worker-svc/worker-svc-0.0.1-dev.jar
