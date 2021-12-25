import pymongo
import os
import jsonlines

myclient = pymongo.MongoClient("mongodb://182.92.1.145:27017/")
mydb = myclient["InformationRetrieval"]
mycol = mydb["citation_test"]

path = 'E:/IRdata/1-100_1/'

files = os.listdir(path)
print(len(files))

for i in range(40, len(files)):
    n = 0

    f = files[i]
    file = path + f
    print(file)
    fr = jsonlines.open(file, 'r')
    mycol.insert_many(fr, ordered=False, bypass_document_validation=True)
    print(i)

