# Information Retrieval - Papers Network

## 1.数据处理模块



## 2.检索模块

### 2.1 检索系统搭建



### 2.2 引文网络子图

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

## 3.前端展示模块



## 小组分工



## 环境部署

### Server

Alibaba Cloud

ip: 182.92.1.145
### MongoDB
port: 27017

### Elastic Search
port: 9200







