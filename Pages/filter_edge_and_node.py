import pandas as pd
import networkx as nx
from pyvis.network import Network
import streamlit as st
import streamlit.components.v1 as components
import math
import matplotlib.pyplot as plt
import numpy as np

HEIGHT = 600
WIDTH = 900

st.set_page_config(layout="wide", page_icon=None, initial_sidebar_state="collapsed", page_title=None)

links = pd.read_csv("Dataset/Links.csv")
nodes = pd.read_csv("Dataset/Nodes.csv")

st.title('Knowledge Graph Analysis')

main_container = st.container()

options_col, chart_col = main_container.columns((1, 2))

with options_col:
    # 创建布局
    edge_type_choice = st.columns(1)
    node_type_choice = st.columns(1)
    #选择边的类型
    edge_types = set(links["type"])
    edge_types.add('all')
    edge_type_choice = st.multiselect("Edge Type:", edge_types)
    #选择节点的类型
    node_types = set(nodes["type"])
    node_types.add('all')
    node_type_choice = st.multiselect("Node Type:", node_types)

    st.divider()# 分割线

    # 滑动条，用于设置权重阈值
    conf_threshold = st.slider('Weight threshold', min_value=0.0000, max_value=1.0, value=0.0000, step=0.0001)

# ----------------------------------- 主要图形逻辑 -----------------------------------
# 根据选定的边类型筛选数据
if 'all' not in edge_type_choice:
    links = links[links["type"].isin(edge_type_choice)]

# 使用选定的 Edge 获取相关节点
selected_nodes_from_edges = set(links['source']).union(set(links['target']))


# 如果未选择所有节点类型，进一步筛选节点
if 'all' not in node_type_choice:
    nodes = nodes[nodes["type"].isin(node_type_choice)]
    selected_nodes = set(nodes['id']).intersection(selected_nodes_from_edges)
else:
    selected_nodes = selected_nodes_from_edges

# 仅保留所选节点的边
links = links[links['source'].isin(selected_nodes) & links['target'].isin(selected_nodes)]

source_list = []
target_list = []
edge_type_list = []

for _, row in links.iterrows():
    if row['weight'] >= conf_threshold:
        source_list.append(row['source'])
        target_list.append(row['target'])
        edge_type_list.append(row['type'])

# 使用 NetworkX 库创建有向图
graph_type = nx.MultiDiGraph()
graph = nx.from_pandas_edgelist(links, 'source', 'target', edge_attr=True, create_using=graph_type)
# ----------------------------------- 主要图形逻辑 -----------------------------------

# ----------------------------------- Pyvis 设置 -----------------------------------
# 创建 Pyvis 网络
with chart_col:
    net = Network(notebook=True, directed=True, height=str(HEIGHT) + "px",
                  width="100%", filter_menu=False, select_menu=False, cdn_resources='remote')

    net.force_atlas_2based(gravity=-10, central_gravity=0.001,
                           spring_length=200, spring_strength=0.01,
                           damping=2, overlap=0)
# ----------------------------------- Pyvis 设置 -----------------------------------

    # 将 nx graph 转换为 pyvis graph
    net.from_nx(graph)

    # 设置箭头大小和箭头长度
    for edge in net.edges:
        edge['arrows'] = 'to'
        edge['arrowStrikethrough'] = True
        edge['scaling'] = {
            'min': 1,
            'max': 5,
            'label': {
                'enabled': True
            }
        }
        edge['color'] = '#808080'  # 设置边的颜色为灰色

    
    # ----------------------------------- 图形颜色逻辑 -----------------------------------
    node_colors = {
        'Mar de la Vida OJSC': '#b96570',#酒红色
        '979893388': '#062d4b',#深蓝色
        'Oceanfront Oasis Inc Carriers': '#248cbf',
        '8327': 'purple'
    }

    node_types_to_colors = {
        'company':'#fcf1f0',
        'organization':'#e4a2b8',
        'person':'#df493f',
        'location':'#b0d992',
        'political_organization':'#f9d580',
        'vessel':'#99b9e9',
        'movement':'#af8fd0',
        'event':'#54beaa',
        'uncategorized':'#eca680'
    }


    # Set the default node size
    default_size = 20  # You can adjust this value based on your preference

    # Set sizes for the 4 specified entities
    specified_entity_sizes = {entity: default_size * 1.5 for entity in node_colors.keys()}

    # Add size attributes to nodes when adding them to the Pyvis graph
    for node in net.nodes:
        if node['id'] in node_colors:
            node['color'] = node_colors[node['id']]
            node['value'] = specified_entity_sizes[node['id']]  # Set size for the specified entities
        else:
            node_type = nodes.loc[nodes['id'] == node['id'], 'type']  # query node type
            node['color'] = node_types_to_colors.get(node_type.values[0])
            node['value'] = default_size  # Set default size for other nodes

    

    # ----------------------------------- 图形颜色逻辑 -----------------------------------


    # ----------------------------------- 保存图形 -----------------------------------
    # 保存为HTML并提供HTML
    html_file = 'graph_analysis.html'
    net.save_graph(html_file)

    legend_html = """
    <div style="position: absolute; top: 20px; left: 20px; z-index: 9999; font-size: 12px; background-color: rgba(255, 255, 255, 0); border-radius: 6px; display: flex; padding: 5px;">
    <div style="margin-right: 20px; flex: 1;">
    """

    for node_type, color in node_types_to_colors.items():
        legend_html += f"<div style='margin: 3px 0; display: flex; align-items: center;'><span style='background-color: {color}; width: 10px; height: 10px; border-radius: 50%; display: inline-block; margin-right: 8px;'></span><span>{node_type}</span></div>"

    legend_html += "</div><div style='flex: 1.5;'>"

    # 为特殊实体添加颜色解释标签
    for entity, color in node_colors.items():
        legend_html += f"<div style='margin: 3px 0; display: flex; align-items: center;'><span style='background-color: {color}; width: 10px; height: 10px;  display: inline-block; margin-right: 8px;'></span><span>{entity}</span></div>"

    legend_html += "</div></div>"

    # 读取原始HTML文件并插入图例HTML
    with open(html_file, "r", encoding="utf-8") as f:
        content = f.read()
        content = content.replace("</body>", legend_html + "</body>")

    # 保存包含图例的新HTML文件
    with open(html_file, "w", encoding="utf-8") as f:
        f.write(content)

    # 显示图形
    HtmlFile = open(html_file, 'r', encoding='utf-8')
    source_code = HtmlFile.read()
    components.html(source_code, height=HEIGHT, width=WIDTH+70)
