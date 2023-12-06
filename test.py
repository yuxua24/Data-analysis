import pandas as pd

# 读取包含数据的DataFrame
df = pd.read_csv('Dataset/MC3/heat_map/country-category_counts.csv')

# 删除除了第一列以外其余列全为0的行
df = df[df.iloc[:, 1:].any(axis=1)]

# 保存结果到新的文件
df.to_csv('Dataset/MC3/heat_map/1.csv', index=False)
