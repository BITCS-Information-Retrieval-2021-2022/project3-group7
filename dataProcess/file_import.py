import pymongo
import os
import jsonlines

myclient = pymongo.MongoClient("mongodb://182.92.1.145:27017/")
mydb = myclient["InformationRetrieval"]
mycol = mydb["citation_es"]

path = 'E:/IRdata/'

files = os.listdir(path)

for i in range(0, len(files)):

    f = files[i]
    file = path + f
    print(file)
    fr = jsonlines.open(file, 'r')
    mycol.insert_many(fr, ordered=False, bypass_document_validation=True)
