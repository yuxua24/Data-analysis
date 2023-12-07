import pandas as pd

# 读取CSV文件
df = pd.read_csv('Dataset/MC3/company.csv')

# 筛选出avg_revenue为0的行
zero_revenue_df = df[df['avg_revenue'] == 0]

# 计算这些行中BOCnt的总和
total_bo_count = zero_revenue_df['BOCnt'].sum()

# 打印结果
print(f"Total number of beneficial owners with avg_revenue of 0: {total_bo_count}")
