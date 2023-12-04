import pandas as pd

# 读取 CSV 文件
df = pd.read_csv('Dataset/MC1/Parallel coordinates/1.csv')


# 获取所有列的名称
columns = list(df.columns)

# 确定最后四列的名称
last_four_columns = columns[-4:]

# 从列名列表中移除最后四列
columns = columns[:-4]

# 将最后四列插入到第 8 到 11 列的位置
# 注意：由于 Python 索引从 0 开始，第 8 列的索引为 7
columns[7:7] = last_four_columns

# 重新排列 DataFrame 的列
df = df[columns]

# 保存更改后的 DataFrame 到 CSV 文件
df.to_csv('Dataset/MC1/Parallel coordinates/2.csv', index=False)


