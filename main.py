# @Time    : 2020/3/7 17:56
# @Author  : gzzang
# @File    : main
# @Project : network_conversion

import numpy as np
import re


flag = False
data = []
with open("SiouxFalls/SiouxFalls_net.tntp", "r") as f:
    for line in f.readlines():
        if flag:
            line = line.strip('\n')
            line = line.strip(';')
            line = line.strip('\t')
            data.append(line.split('\t'))
        flag = not flag if line[0] == '~' else flag

link_list_node_pair = [(int(one_data[0]), int(one_data[1])) for one_data in data]
link_capacity = [float(one_data[2]) for one_data in data]
link_free_flow_time = [float(one_data[4]) for one_data in data]

print(link_list_node_pair)
print(link_capacity)
print(link_free_flow_time)

flag = False
data = []
with open("SiouxFalls/SiouxFalls_trips.tntp", "r") as f:
    for line in f.readlines():
        if not flag:
            flag = not flag if line[0] == 'O' else flag
        if flag:
            if 'Origin' in line:
                if '1' not in line:
                    data.append(one_data)
                one_data = []
            else:
                line = line.strip('\n')
                line = line.replace(' ', '')
                line = re.split('[:;]', line)
                del (line[-1])
                for index, value in enumerate(line):
                    if index % 2:
                        one_data.append(float(value))

od_demand = np.array(data)
node_number = od_demand.shape[0]
od_list_node_pair = []
od_list_demand = []
for i in range(node_number):
    for j in range(node_number):
        if od_demand[i, j] != 0:
            od_list_node_pair.append((i, j))
            od_list_demand.append(od_demand[i, j])

print(od_list_node_pair)
print(od_list_demand)
