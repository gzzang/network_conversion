# 网络转换
将tntp格式转换为csv格式和pickle格式

需要分别读取行程和节点的数据

行程数据基于OD矩阵比较复杂

节点数据基于csv格式可直接读取

做了比较发现，用pandas都csv比按文件读慢10倍

tntp格式是源数据的格式

csv格式存储简单清晰

pickle格式存储读取方便