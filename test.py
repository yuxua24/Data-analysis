import pandas as pd

# 读取CSV文件
df = pd.read_csv('Dataset/MC3/2.csv')

# 计算平均收入
# 使用numpy的where函数来进行条件选择
# 如果BOCnt不为0，使用revenue_omu / BOCnt，否则使用revenue_omu / CCCnt
df['average_income'] = df.apply(
    lambda row: row['revenue_omu'] / row['BOCnt'] if row['BOCnt'] != 0 else row['revenue_omu'] / row['CCCnt'], 
    axis=1
)

# 将结果保存到新的CSV文件
df.to_csv('Dataset/MC3/3.csv', index=False)



