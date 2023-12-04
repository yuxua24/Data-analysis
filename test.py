import pandas as pd

# 读取 CSV 文件
df = pd.read_csv('Dataset/MC1/community2/community_edge_node_stats_full_bin.csv')

# 删除第五列
# 注意：由于 Python 索引从 0 开始，第五列的索引为 4
df.drop(df.columns[7], axis=1, inplace=True)

# 保存更改后的 DataFrame 到 CSV 文件
df.to_csv('Dataset/MC1/community2/1.csv', index=False)
