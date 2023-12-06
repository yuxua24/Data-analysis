import csv

# 输入和输出文件名
input_file = 'Dataset/MC3/4.csv'
output_file = 'Dataset/MC3/5.csv'

# 打开输入文件和输出文件
with open(input_file, 'r') as csv_in_file, open(output_file, 'w', newline='') as csv_out_file:
    reader = csv.reader(csv_in_file)
    writer = csv.writer(csv_out_file)
    
    # 写入第一行（标题行）
    header = next(reader)
    writer.writerow(header)

    # 遍历每一行数据
    for row in reader:
        # 计算除第一列外其他列的总和
        total = sum(map(float, row[1:]))
        
        # 检查总和是否不超过10
        if total > 10:
            # 如果是，将这一行写入输出文件
            writer.writerow(row)

print(f"已删除除了第一列其他列相加总数不超过10的行，并将结果保存到{output_file}")
