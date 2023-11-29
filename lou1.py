import pandas as pd
import networkx as nx
from community import community_louvain
import numpy as np

# 读取边列表数据
edges_df = pd.read_csv('Dataset/Links.csv')

# 创建有向图
G = nx.from_pandas_edgelist(edges_df, 'source', 'target', ['weight'], create_using=nx.MultiDiGraph())

# 将有向图转换为无向图
G_undirected = G.to_undirected()

# 迭代次数
iterations = 1000

# 创建一个初始的 partition 字典，将所有节点分配到默认社区
partition = {node: node for node in G_undirected.nodes()}

for i in range(iterations):
    # 应用Louvain社区检测算法
    new_partition = community_louvain.best_partition(G_undirected, partition=partition)
    # 统计每个社区的节点数量
    community_sizes = {community: sum(1 for node in new_partition if new_partition[node] == community)
                       for community in set(new_partition.values())}
    
    # 找到节点数小于100的社区
    small_communities = [community for community, size in community_sizes.items() if size < 100]
    nodes_to_remove = []
    
    # 遍历小社区并检查边的权重
    for community in small_communities:
        # 获取社区内的节点列表
        community_nodes = [node for node in new_partition if new_partition[node] == community]
        
        # 获取社区内的所有边的权重
        weights = []
        for node1 in community_nodes:
            for node2 in community_nodes:    
                if node1 != node2 and G_undirected.has_edge(node1, node2):
                   weights.append(G_undirected[node1][node2][0]['weight'])
        
        if len(weights) > 0:
            mu = np.mean(weights)  # 计算均值
            sigma = np.std(weights)  # 计算标准差
            
            # 检查社区中所有边是否都在 [μ - 3σ, μ + 3σ] 区间内
            if all(mu - 3 * sigma <= weight <= mu + 3 * sigma for weight in weights):
                # 删除这个社区中的节点
                for node in new_partition:
                    if new_partition[node] == community:
                        nodes_to_remove.append(node)

    # 在迭代完成后删除节点
    for node in nodes_to_remove:
        del new_partition[node]
    # 更新分区
    partition = new_partition
    # 在每轮迭代后，根据新的 partition 创建一个新图
    nodes_to_keep = set(new_partition.keys())
    G_undirected = G_undirected.subgraph(nodes_to_keep)

# 保存最终的社区分类为CSV
community_df = pd.DataFrame(partition.items(), columns=['Node', 'Community'])
community_df.to_csv(f'Louvain_{iterations}_iterations.csv', index=False)

print(f"{iterations} iterations of Louvain algorithm have been completed, and the final community partition has been saved!")