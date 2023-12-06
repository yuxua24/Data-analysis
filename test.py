import pandas as pd

# 读取包含数据的DataFrame
df = pd.read_csv('Dataset/MC3/nodes.csv')


# 使用groupby和count来统计国家为空值的各种类型的数量
result = df[df['country'].isnull()].groupby('type').size().reset_index(name='count')

# 打印结果
print(result)
