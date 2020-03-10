# @Time    : 2020/3/10 10:49
# @Author  : gzzang
# @File    : read_flow
# @Project : network_conversion

# 读取流量与计算结果进行对比

import pandas as pd
import pickle

file_path = f'network/SiouxFalls/SiouxFalls_flow.tntp'

flow_df = pd.read_csv(file_path, delimiter='\t')
flow_df.columns = flow_df.columns.str.strip(' ')
flow = flow_df['Volume'].to_numpy()

with open(f'output/siouxfalls_flow.pkl', 'wb') as f:
    pickle.dump(flow, f)
