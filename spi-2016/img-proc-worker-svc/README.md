## Worker Service

This service read messages from a rabbitmq queue.
Expected message content is a json like this:

```shell
{
    "jobId": "8a0d53bb-1716-4fd8-8214-03d3462b2044",
    "filterId": "Filter 1",
    "originalImageUrl": "http://storage-svc:8083/file/71cb59ca-f425-43d1-b30a-d0f3a83a1967.jpeg"
}
```

Service operation is like this:
 - download file from storage-svc using originalImageUrl
 - process the file according to filterId
 - store the new processed file into storage-svc
 - Update job with id equal to jobId setting resultImageUrl
   and status = "PROCESSED"
