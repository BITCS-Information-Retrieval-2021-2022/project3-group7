# coding:utf-8

from pyspark import SparkContext, SparkConf, SQLContext
from pyspark.sql import SparkSession
from pymongo import *


# 配置
def conf():
    conf = SparkConf().setAppName('IR').setMaster("local[*]")
    my_spark = SparkSession.builder \
        .config(conf=conf) \
        .config("spark.mongodb.input.uri", "mongodb://182.92.1.145:27017/InformationRetrieval.citation00") \
        .config("spark.mongodb.output.uri", "mongodb://182.92.1.145:27017/InformationRetrieval.citation00") \
        .config("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.12:3.0.1") \
        .getOrCreate()

    sql = SQLContext(my_spark)

    return my_spark, sql


# 数据读取
def read_data(spark):
    df = (
        spark.read
        .format('mongo')
        .option("database", 'InformationRetrieval')
        .option("collection", 'citation00')
        .load()
    )

    df.createOrReplaceTempView('view')
    resDf = spark.sql('select Sid,outCitations from view')
    data = resDf.rdd.collect()
    list = []

    for i in data:
        point_list = []
        point_list.append(i[0])
        point_list.append(tuple(i[1]))
        list.append(tuple(point_list))
    spark.stop()

    return list


def f(x):
    list1 = []
    s = len(x[1][0])
    for y in x[1][0]:
        list1.append(tuple((y, x[1][1] / s)))

    return list1


def PageRank(list):
    conf = SparkConf()
    conf.setMaster("spark://iZ2zees9oqwpuri28nvwwmZ:7077")
    conf.setAppName("PageRank")

    sc = SparkContext(conf=conf)

    node = []
    for i in list:
        node.append(i[0])

    pages = sc.parallelize(list).map(lambda x: (x[0], tuple(x[1]))).partitionBy(20).cache()

    # 初始PR值为1
    links = sc.parallelize(node).map(lambda x: (x, 1.0))

    # 迭代
    for i in range(0, 2):
        rank = pages.join(links).flatMap(f)
        links = rank.reduceByKey(lambda x, y: x + y)
        links = links.mapValues(lambda x: 0.15 + 0.85 * x)
    j = links.collect()

    return j


# 添加重要性分数
def addImportValue(col):

    client = MongoClient("mongodb://182.92.1.145:27017/")
    db_name = 'InformationRetrieval'
    db = client[db_name]
    collection = db['test01']

    for i in col:
        collection.update_one({'Sid': i[0]}, {'$set': {'importantValue': i[1]}})
    print('Over')


if __name__ == "__main__":

    spark, _ = conf()
    list = read_data(spark)
    value_col = PageRank(list)
    addImportValue(value_col)

