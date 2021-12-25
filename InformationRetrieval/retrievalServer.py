from flask import Flask, request, jsonify
from settings import parameters
from esClient import ESClient
from dbAccess import DBAccess
from utils import genQuery
import json

app = Flask(__name__)

es = ESClient(hosts=parameters['host'],
              port=parameters['es_port'],
              user=parameters['es_user'],
              password=parameters['password'],
              index=parameters['papers_index'])

db = DBAccess(hosts=parameters["mongo_host"],
              port=parameters["db_port"],
              user=parameters["db_user"],
              password=parameters["db_password"],
              db_name=parameters["db_name"],
              doc_name=parameters["papers_doc"])


@app.route('/query', methods=['GET'])
def retrievalPaper():
    query = genQuery()
    query['hits'] = es.search(query)
    res = db.search(query)
    return json.dumps(res)


@app.route('/networks', methods=['GET'])
def retrievalNetworks():
    query = genQuery()
    """
    There should be some methods to generate networks.
    """
    res = db.get_network(query)
    json_data = json.dumps(res)
    json_data = json_data.replace('title', 'id')
    return json_data


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=parameters["flask_port"])