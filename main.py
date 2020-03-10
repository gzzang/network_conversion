# @Time    : 2020/3/7 17:56
# @Author  : gzzang
# @File    : main
# @Project : network_conversion

# 矩阵不全

import numpy as np
import pickle
import os
import pandas as pd

source_network_name = 'ChicagoSketch'
# source_network_name = 'SiouxFalls'

source_folder_path = 'network/' + source_network_name + '/'
source_link_file_path = source_folder_path + source_network_name + '_net.tntp'
source_od_file_path = source_folder_path + source_network_name + '_trips.tntp'

output_folder_path = f'output/'
network_name = source_network_name.lower()
output_link_file_path = output_folder_path + network_name + '_link.csv'
output_od_file_path = output_folder_path + network_name + '_od.csv'

output_network_pickle_file_path = output_folder_path + network_name + '.pkl'

if not os.path.exists(output_folder_path):
    os.mkdir(output_folder_path)

# 读取link信息
flag_data = False
line_data = []
with open(source_link_file_path, "r") as f:
    for line in f.readlines():
        if flag_data:
            line = line.strip('\n')
            line = line.strip(';')
            line = line.strip('\t')
            line_data.append(line.split('\t'))
        flag_data = not flag_data if line[0] == '~' else flag_data

link_node_pair = np.array([(int(one_data[0]) - 1, int(one_data[1]) - 1) for one_data in line_data])
link_capacity = np.round(np.array([float(one_data[2]) for one_data in line_data]))
link_free_flow_time = np.array([float(one_data[4]) for one_data in line_data])

link_number = len(link_node_pair)
link_array = np.hstack(
    (np.array(link_node_pair), link_free_flow_time.reshape([link_number, 1]), link_capacity.reshape([link_number, 1])))

# 存储link信息
link_df = pd.DataFrame()
link_df = pd.concat([link_df, pd.DataFrame(columns=['init_node', 'term_node'], data=link_node_pair)])
link_df['free_flow_time'] = np.array([float(one_data[4]) for one_data in line_data])
link_df['capacity'] = np.array([float(one_data[2]) for one_data in line_data])
link_df.to_csv(output_link_file_path, index=False)

# 读取od信息
flag_data = False
od_list_node_pair = []
od_list_demand = []
with open(source_od_file_path, "r") as f:
    for line in f.readlines():
        if not flag_data:
            flag_data = not flag_data if line[0] == 'O' else flag_data
        if flag_data:
            if 'Origin' in line:
                init_index = int(line[6:]) - 1
            else:
                line = line.strip('\n')
                line = line.replace(' ', '')
                line = line.split(';')
                del (line[-1])
                for str in line:
                    str2 = str.split(':')
                    if float(str2[1]) != 0:
                        od_list_node_pair.append([init_index, int(str2[0]) - 1])
                        od_list_demand.append(float(str2[1]))

od_node_pair = np.array(od_list_node_pair)
od_demand = np.array(od_list_demand)

# 存储od信息
od_df = pd.DataFrame()
od_df = pd.concat([od_df, pd.DataFrame(columns=['init_node', 'term_node'], data=od_node_pair)])
od_df['demand'] = od_demand
od_df.to_csv(output_od_file_path, index=False)

# 存储pickle
data = {'link_node_pair': link_node_pair, 'link_capacity': link_capacity, 'link_free_flow_time': link_free_flow_time,
        'od_node_pair': od_node_pair, 'od_demand': od_demand}
with open(output_network_pickle_file_path, 'wb') as f:
    pickle.dump(data, f)
