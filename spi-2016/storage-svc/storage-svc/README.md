## Example queries

### Store a new file
```shell
curl -v -X POST -H 'Content-Type: application/json' http://127.0.0.1:8083/files -d '{"content":"<fileContentBase64Encoded>",
"contentType":"image/jpeg"
}' | python -m json.tool

Response: {"status": "OK", "fileId": "f5f5a010-0426-4730-9415-257b5a47891e.jpeg"}
```

### get stored file
```shell
curl -v -X GET -H 'Accept: application/json' http://127.0.0.1:8083/files/435854d8-32df-4ae3-a059-e109ae8e9369.jpg
```
