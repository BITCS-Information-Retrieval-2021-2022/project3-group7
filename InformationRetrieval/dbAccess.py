import pymongo
from bson.objectid import ObjectId
from settings import parameters
import json
import math

RULE = {
    "1": {
        "size": 10,
        "minValue": 0.15,
        "maxNum": 25,
        "proportionNum": 0.50
    },
    "2": {
        "size": 5,
        "minValue": 0.30,
        "maxNum": 20,
        "proportionNum": 0.30
    },
    "3": {
        "size": 2.5,
        "minValue": 0.45,
        "maxNum": 15,
        "proportionNum": 0.15
    }
}


class DBAccess:
    def __init__(self, **kwargs):
        self.hosts = kwargs['hosts']
        self.port = kwargs['port']
        # self.user = kwargs['user']
        # self.password = kwargs['password']
        self.dbName = kwargs['db_name']
        self.docName = kwargs['doc_name']
        connect_string = "mongodb://{}:{}/{}".format(self.hosts, self.port, self.dbName)
        self.dbClient = pymongo.MongoClient(connect_string)
        self.db = self.dbClient[self.dbName]
        self.doc = self.db[self.docName]

    # 通过检索得到的论文id列表获取对应文档信息列表
    def search(self, query):
        """
        According to es _id lists, get mongodb doc lists.(change query['hits']['hit'])
        :param hit_id: _id
        :return: citation subgraph
        """
        idList = query['hits']['hit']
        res = []
        for id in idList:
            dbQuery = {"_id": id if isinstance(id, ObjectId) else ObjectId(id)}  # 获取ObjectId
            res.append(self.doc.find_one(dbQuery), {"_id": 0})  # 返回_id对应的单个文档
        # res = self.reformatResult(res)
        query['hits']['hit'] = res
        return query

    def reformatResult(self, res):
        """
        According to res, change value type to return.
        :param res: result
        :return: reformatted result
        """
        return res

    # 以选中论文为中心节点生成引文网络子图：
    # 1.包括之前和之后节点
    # 2.根据节点互相引用关系、节点重要性筛选出一定数量的节点用于展示
    # 3.提供引文网络子图的节点和边的信息
    def get_network(self, query):
        """
        According to Sid, get mongodb doc lists.(change query['hits']['hit'])
        :param  hit Sid
        :return: citation subgraph
        """
        center = self.doc.find_one({"Sid": query["query"]}, {"_id": 0})  # 选中的中心节点
        if center:  # 如果查询到对应的中心论文节点
            center['size'] = 20
            center['group'] = math.floor(center['importantValue'] * 5)
            query['subgraph']['nodes'].append(center)
            # 第一层
            in_nodes1, out_nodes1 = self.citation(query, center, '1')
            # 第二层
            for id1 in in_nodes1 + out_nodes1:
                # print("2", id1)
                node1 = self.doc.find_one({"Sid": id1}, {"_id": 0})
                if node1:
                    in_nodes2, out_nodes2 = self.citation(query, node1, '2')
                    # 第三层
                    for id2 in in_nodes2 + out_nodes2:
                        # print("3", id2)
                        node2 = self.doc.find_one({"Sid": id2}, {"_id": 0})
                        if node2:
                            in_nodes3, out_nodes3 = self.citation(query, node2, '3')
        query['subgraph']['nodeCount'] = len(query['subgraph']['nodes'])
        query['subgraph']['linksCount'] = len(query['subgraph']['links'])
        return query

    # 获取并筛选某个文档的引用与被引
    def citation(self, query, node, layer):
        in_nodes = []
        out_nodes = []
        in_num_flag = True
        out_num_flag = True
        if node['inCitationsCount'] > RULE[layer]['maxNum']:
            in_num_flag = False
            in_num_res = RULE[layer]['maxNum'] + math.floor(
                (node['inCitationsCount'] - RULE[layer]['maxNum']) * RULE[layer]['proportionNum'])
        if node['outCitationsCount'] > RULE[layer]['maxNum']:
            out_num_flag = False
            out_num_res = RULE[layer]['maxNum'] + math.floor(
                (node['outCitationsCount'] - RULE[layer]['maxNum']) * RULE[layer]['proportionNum'])
        for c_in in node['inCitations']:
            flag = True
            if (not in_num_flag) and len(in_nodes) >= in_num_res:
                flag = False
            if flag:
                in_doc = self.doc.find_one({"Sid": c_in}, {"_id": 0})
                if in_doc:
                    if in_doc['importantValue'] > RULE[layer]['minValue']:
                        in_nodes.append(c_in)
                        in_doc['size'] = RULE[layer]['size']
                        in_doc['group'] = math.floor(in_doc['importantValue'] * 5)
                        query['subgraph']['nodes'].append(in_doc)
                        query['subgraph']['links'].append({"source": node['title'], "value": 1, "target": in_doc['title']})
        for c_out in node['outCitations']:
            flag = True
            if (not out_num_flag) and len(out_nodes) >= out_num_res:
                flag = False
            if flag:
                out_doc = self.doc.find_one({"Sid": c_out}, {"_id": 0})
                if out_doc:
                    if out_doc['importantValue'] > RULE[layer]['minValue'] and flag:
                        out_nodes.append(c_out)
                        out_doc['size'] = RULE[layer]['size']
                        out_doc['group'] = math.floor(out_doc['importantValue'] * 5)
                        query['subgraph']['nodes'].append(out_doc)
                        query['subgraph']['links'].append({"source": out_doc['title'], "value": 1, "target": node['title']})
        return in_nodes, out_nodes


# def __del__(self):
#     self.dbClient.close()
#     print("Notice from DBAccess: MongoDB connection is closed.")


# dbAccess测试
if __name__ == "__main__":
    db = DBAccess(hosts=parameters["mongoHost"],
                  port=parameters["dbPort"],
                  user=parameters["dbUser"],
                  password=parameters["dbPassword"],
                  db_name=parameters["dbName"],
                  doc_name=parameters["papersDoc"])
    query = dict()
    query = {
        "query": "f6370fe63ff9c7191335c3e5de8d4b6935ae1792",  # 选中中心论文的Sid  f6370fe63ff9c7191335c3e5de8d4b6935ae1792
        "subgraph": {
            "nodeCount": 0,  # 子图节点个数
            "nodes": [],  # 子图节点列表
            "linksCount": 0,  # 三元组个数
            "links": []  # 三元组列表（节点和边）
        }
    }
    db.get_network(query)
    json_data = json.dumps(query, indent=2)
    json_data = json_data.replace('title', 'id')
    print(json_data)
    with open('sub1.json', 'w') as f:
        f.write(json_data)
