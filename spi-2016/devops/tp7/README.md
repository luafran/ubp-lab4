### InfluxDB dashboard

http://localhost:8083/

### Grafana Dashboard

http://localhost:3000/

### Kibana Dashboard

http://localhost:5601


### Test logging using one-shot container

```shell
docker run --log-driver gelf --log-opt gelf-address=udp://127.0.0.1:12201 --rm alpine echo hello world
```