
### Example queries

```shell
curl -v -X GET -H 'Accept: application/json' http://127.0.0.1:8082/jobs | python -m json.tool
curl -v -X POST -H 'Content-Type: application/json' http://127.0.0.1:8082/jobs -d '{"originalImageUrl": "originalUrl", "filterId": "1", "resultImageUrl": "resultUrl"}' | python -m json.tool
curl -v -X GET -H 'Accept: application/json' http://127.0.0.1:8082/jobs/435854d8-32df-4ae3-a059-e109ae8e9369 | python -m json.tool
```