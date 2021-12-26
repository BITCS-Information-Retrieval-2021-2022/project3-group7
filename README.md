# Information Retrieval - Papers Network

## 一、数据处理模块

## 项目部署过程

### 1 MongoDB数据库

#### 1.1 安装包下载

Step1：在Linux官网下载与操作系统版本匹配的mongodb数据库。（项目使用64位 Ubuntu系统）

Step2：使用xftp将安装包上传至/usr/local/mongodb目录下。

Step3：解压缩，并将解压包移动到指定目录。

```
tar zxvf mongodb-linux-x86_64-ubuntu2004-5.0.5.tgz # 解压
mv mongodb-linux-x86_64-ubuntu2004-5.0.5/ /usr/local/mongodb # 移动到指定目录
```

Step4：创建数据文件夹和日志文件、配置文件。

```
mkdir -p /usr/local/mongodb/data
touch /usr/local/mongodb/mongod.log
touch /usr/local/mongodb/mongodb.conf
```

#### 1.2 系统profile配置

Step1：打开系统配置文件profile进行编辑。

```
# 打开系统配置文件
vim /etc/profile
# 点击Insert，并输入以下内容
export PATH=$PATH:/usr/local/mongodb/mongodb-linux-x86_64-ubuntu2004-5.0.5/bin
# 点击键盘esc键进行命令执行，输入:wq 进行保存并退出
```

Step2：重启系统配置

```
source /etc/profile
```

#### 1.3 MongoDB启动配置

Step1：进入MongoDB数据库安装目录的bin文件夹中。

```
cd /usr/local/mongodb/mongodb-linux-x86_64-ubuntu2004-5.0.5/bin
```

Step2：修改MongoDB配置文件。

```
# 打开配置文件
/usr/local/mongodb/mongodb.conf
# 在配置中加入以下代码
dbpath=/usr/local/mongodb/data # 数据文件存放的绝对路径
logpath=/usr/local/mongodb/mongod.log # 日志文件存放的绝对路径
logappend=true # 追加日志
port=27017 # 端口
fork=true # 以守护程序的方式启用，即在后台运行
quiet=true
bind_ip=0.0.0.0 # 绑定地址
```

### 2 JDK

版本：1.8.0_221

安装过程：

Step1：下载JDK安装包jdk-8u221-linux-x64.tar.gz。

Step2：前往安装包所在目录解压。
```
tar -zxvf jdk-8u221-linux-x64.tar.gz
```

Step3：配置环境变量。

```
# 打开系统配置文件Profile
vim /etc/profile

# 在配置文件中添加以下代码
export JAVA_HOME=/root/jdk1.8.0_221
export CLASSPATH=.:$JAVA_HOME/jre/rt.jar:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar
export PATH=$PATH:$JAVA_HOME/bin

# 重新加载配置文件
source /etc/profile
```

### 3 Hadoop

版本：3.3.1


#### 3.1 设置SSH无密码登录

Step1:安装SSH server
```
sudo apt-get install openssh-server
```
Step2:生成密钥对
```
ssh-keygen -t rsa -P ”-f ~/.ssh/id_rsa
```
Step3:生成验证密钥
```
cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
```

Step4:修改文件权限
```
chmod 0600 ~/.ssh/authorized_keys
```

Step5:验证
```
ssh localhost
```

#### 3.2 下载安装hadoop

Step1：下载安装包hadoop-3.3.1.tar.gz。

Step2：解压并更改安装目录。
```
tar -zxvf hadoop-3.3.1.tar.gz -C /usr/local
```
Step3：修改目录名称。
```
mv hadoop-3.3.1 hadoop
```
Step4：修改文件权限。
```
sudo chown -R root ./hadoop
```
Step5：验证是否安装成功。
```
# 进入hadoop安装目录
./bin/hadoop version
```
若出现hadoop版本信息，证明hadoop可用

#### 3.3 hadoop伪分布式安装

Step1：声明JDK环境，在hadoop/etc/hadoop/hadoop-env.sh配置文件中添加JAVA_HOME。

Step2：修改配置文件。
```
# 进行hadoop安装目录，修改hadoop/etc/hadoop/core-site.xml配置文件
<configuration>
	<property>
		<name>fs.default.name</name>
		<value>hdfs://localhost:9000</value>
		<description>指定HDFS的默认名称</description>
	</property>
	<property>
		<name>fs.defaultFS</name>
		<value>hdfs://localhost:9000</value>
		<description>HDFS的URI</description>
	</property>
	<property>
		<name>hadoop.tmp.dir</name>
		<value>/usr/local/hadoop/tmp</value>
		<description>节点上本地的hadoop临时文件夹</description>
	</property>
</configuration>
```
```
# 修改hadoop/etc/hadoop/hdfs-site.xml配置文件
<configuration>
	<property>
		<name>dfs.namenode.name.dir</name>
		<value>file:/usr/local/hadoop/hdfs/name</value>
		<description>namenode上存储hdfs名字空间元数据 </description>
	</property>
	<property>
		<name>dfs.datanode.data.dir</name>
		<value>file:/usr/local/hadoop/hdfs/data</value>
		<description>datanode上数据块的物理存储位置</description>
	</property>
	<property>
       <name>dfs.replication</name>
        	<value>1</value>
		<description>副本个数，默认是3,应小于datanode机器数量</description>
	</property>
</configuration>
```
Step3：格式化文件系统。

在hadoop安装目录下，对namenode进行格式化
```
sudo ./bin/hdfs namenode -format
```
启动NameNode守护进程和DataNode守护进程
```
sudo ./sbin/start-dfs.sh
```

### 4 Scala

Step1：下载Spark安装包  https://spark.apache.org/downloads.html。

Step2：使用xftp将安装包上传至/usr/local/src目录下并解压。

```
tar -zxvf scala-2.12.0.tgz
```

Step3：配置环境变量。

```
# 打开系统配置文件profile
vim /etc/profile
# 在配置文件中添加以下代码
export SCALA_HOME=/usr/local/src/scala-2.12.0
export PATH=$PATH:$SCALA_HOME/bin
```

### 5 Spark

Step1：下载Spark安装包  https://www.scala-lang.org/。

Step2：使用xftp将安装包上传至/usr/local/src目录下并解压。

```
tar -zxvf spark-3.2.0-bin-hadoop3.2.tgz
```

Step3：配置环境变量。

```
# 打开系统配置文件Profile
vim /etc/profile
# 在配置文件中添加以下代码
export SPARK_HOME=/usr/local/src/spark-3.2.0-bin-hadoop3.2
export PATH=$PATH:$SPARK_HOME/bin
export PATH=$PATH:$SPARK_HOME/sbin
```

Step4：Spark配置。

```
# 打开Spark配置文件
vim /usr/local/src/spark-3.2.0-bin-hadoop3.2/conf/spark-env.sh
# 在配置文件中添加以下代码
export JAVA_HOME=/root/jdk1.8.0_221
export SCALA_HOME=/usr/local/src/scala-2.12.0
HADOOP_HOME=/usr/local/hadoop
HADOOP_CONF_DIR=/usr/local/hadoop/etc/hadoop
SPARK_MASTER_IP=182.92.1.145
SPARK_MASTER_PORT=7077
SPARK_WORKER_MEMORY=1g   #spark里许多用到内存的地方默认1g 2g 这里最好设置大与1g
```



## 启动运行流程

### 1 启动MongoDB服务

Step1：进入MongoDB数据库安装目录下，打开bin文件夹。

```
cd /usr/local/mongodb/mongodb-linux-x86_64-ubuntu2004-5.0.5/bin
```

Step2：在终端输入以下命令启动MongoDB数据库服务，其中 **/usr/local/mongodb/mongodb.conf** 为数据库配置文件的绝对路径。

```
./mongod --config /usr/local/mongodb/mongodb.conf
```

Step3：停止服务。

```
./mongod --config /usr/local/mongodb/mongodb.conf
```

### 2 启动Hadoop服务

进入Hadoop安装目录下，输入以下命令启动namenode和datanode。

```
 ./sbin/start-dfs.sh
```
输入jps，出现namenode及datanode证明启动成功.

### 3 启动Spark服务

Step1：进入Spark安装目录下，打开Sbin文件夹。

```
cd /usr/local/src/spark-3.2.0-bin-hadoop3.2/sbin
```

Step2：在终端输入以下命令启动Spark服务。

```
./start-all.sh
```

## 节点重要性分数算法
### 1 RDD分区方式
Spark程序可以通过控制RDD分区方式来减少通信开销，提高整体性能。RDD即弹性分布式数据集，是spark对于分布式数据集的抽象，主要特性就是对数据进行分区计算。
### 2 算法流程

我们结合RDD分区方式使用PageRank算法来对引文网络的节点重要性进行计算。

Step1：从数据集中取出节点的Sid以及outCitations，将其转化为RDD计算所需的键值对形式，即(Sid, outCitations)。

Step2：将每个节点的权重值初始化为1.0。

Step3：在每次迭代中，对节点p，向其每个出链指向的节点发送一个rank(p)/neighborsSize(p)的贡献值，记为contributionReceived。

Step4：将每个节点的权重值重新设置为：0.15 + 0.85 *contributionReceived。

Step5：重复Step3和Step4两个步骤，在迭代中，算法逐渐收敛于每个节点的实际PageRank值。

Step6：得到各节点的重要性分数后，将其写入数据库。

## 二、检索模块

### 1 检索系统搭建

**检索系统搭建流程**

*Step1*: 创建MongoDB的存放数据的view:

```
db.createView(
    "papersView",
    "papers",
    [{$project: {
        "Sid": 1,
        "title": 1,
        "year": 1,
        "inCitationsCount": 1,
        "outCitationsCount": 1,
        "importantValue": 1}
    }
    ]
)
```

*Step2*: 创建对应es的mapping:

```
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
```

*Step3*: 使用monstache将mongoDB和es建立连接（monstache的配置文件见代码文件），将mongoDB中的数据同步至es中。

*Step4*: 构建一个flask服务，与前端进行连接，在收到前端的请求后，对请求进行解析并进行对应的检索和取数据操作。以检索RetrievalPapers为例，在得到检索关键词后，调用es的检索函数es.search进行检索，检索成功后，再前往mongoDB中查找数据，最后整理数据格式以json格式返回给前端。

### 2 引文网络子图

**生成引文网络子图算法流程**

*Step1*：从中心节点出发，按照节点筛选算法筛选中心节点的引用和被引节点，作为第一层；

*Step2*：遍历第一层筛选得到的节点，以该节点为查询节点，进行节点筛选，作为第二层；

*Step3*：同*Step2*，对第二层筛选的节点进行遍历，作为第三层；

**节点筛选算法流程**（以被引节点为例）

*Step1*：设置以查询节点为中心的节点数量阈值，若被引节点总数量大于节点数量阈值maxNum，则超出部分按照设定占比proportionNum重新计算更新节点数量阈值in_num_res，反之；

*Step2*：遍历被引节点；

​		判断当前已保存的被引节点数量是否超出阈值in_num_res，若超出阈值，则停止筛选，返回保存的被引节点列表，反之；

​		判断被引节点重要性分数是否大于minValue，若是，则保存该被引节点，反之；

```python
# 节点筛选规则：三层
RULE = {
    "1": {
        "size": 10,           # 设置节点大小
        "minValue": 0.15,     # 重要性分数最小阈值
        "maxNum": 25,         # 节点数量最大阈值
    	"proportionNum": 0.50 # 超出节点数量限制的节点占比 
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
```

## 三、前端展示模块



## 小组分工

数据处理：薛新月、侯晋宏

检索与引文网络：卢一凡、郭倞涛

前端展示：田宇航、杨成


## 环境部署

### Server

Alibaba Cloud

ip: 182.92.1.145

### MongoDB
port: 27017

### Elastic Search
port: 9200








