curl -X DELETE localhost:9200/papers
curl -H 'Content-Type: application/json' -X PUT 'localhost:9200/papers?pretty' -d'
{
    "mappings": {
        "dynamic": "strict",
        "properties": {
            "Sid": {"type": "keyword", "index": false},
            "title": {"type": "text"},
            "year": {"type": "short"},
            "inCitationsCount": {"type": "short", "index": false},
            "outCitationsCount": {"type": "short", "index": false},
            "importantValue": {"type": "double"}
        }
    }
}'
