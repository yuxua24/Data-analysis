import csv

# 读取Nodes.csv文件并将节点存储到集合中
nodes_set = set()
with open('Dataset/MC3/nodes.csv', 'r',encoding='utf-8') as nodes_file:
    csv_reader = csv.reader(nodes_file)
    for row in csv_reader:
        nodes_set.add(row[0])  # 假设节点在每行的第一列

# 读取Links.csv文件并统计没有出现在Nodes.csv中的节点数量
missing_nodes_count = 0
with open('Dataset/MC3/links.csv', 'r',encoding='utf-8') as links_file:
    csv_reader = csv.reader(links_file)
    for row in csv_reader:
        source_node, target_node = row[0], row[1]  # 假设源节点和目的节点在每行的第一列和第二列
        if source_node not in nodes_set:
            missing_nodes_count += 1
        if target_node not in nodes_set:
            missing_nodes_count += 1

print(missing_nodes_count)
