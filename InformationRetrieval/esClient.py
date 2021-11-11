from elasticsearch import Elasticsearch


class ESClient:
    def __init__(self, **kwargs):
        self.hosts = kwargs['hosts']
        self.port = kwargs['port']
        self.user = kwargs['user']
        self.passwords = kwargs['password']
        self.index = kwargs['index']
        self.es = Elasticsearch(hosts=self.hosts,
                                http_auth=(self.user, self.passwords),
                                port=self.port)

    def search(self, query):  # Noticed that logic of retrieval might need resetting or setting more carefully.
        es_query = {
            "track_total_hits": "true",
            "from": 0,
            "size": query["size"],
            "query": {
                "bool": {
                    "must": [
                        {
                            "function_score": {
                                "query": {
                                    "bool": {}
                                },
                                "functions": {
                                    "field_value_factor": {
                                        "field": "click_num",
                                        "modifier": "log1p",
                                        "missing": 1
                                    }
                                }
                            }
                        }
                    ]
                }
            },
            "sort": [
                {
                    "importance_score": "true"  # assumption index: importance_score
                }
            ]
        }

        core_query = [
            {"match": {"title": {"query": query["query"], "boost": 2.0, "operator": "or", "minimum_should_match": "80%"}}}  # should be set more carefully
        ]
        es_query["query"]["bool"]["must"][0]["function_score"]["query"]["bool"]["should"] = core_query
        res = self.es.search(index=self.index, body=es_query)

        id_list = [item["_id"] for item in res["hits"]["hits"]]

        hit = {"total": res["hits"]["total"]["value"], "hit": id_list}
        return hit

    def __del__(self):
        self.es.close()
        print("Notice from ESClient: Elasticsearch is closed.")