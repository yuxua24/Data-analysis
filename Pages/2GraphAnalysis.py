import pandas as pd
import networkx as nx
from pyvis.network import Network
import streamlit as st
import streamlit.components.v1 as components
import math
import matplotlib.pyplot as plt
import numpy as np
from streamlit_echarts import st_pyecharts
from pyecharts.charts import Bar,Tab
from pyecharts import options as opts

HEIGHT = 1500
WIDTH = 900

st.set_page_config(layout="wide", page_icon=None,
                   initial_sidebar_state="collapsed", page_title=None)

links = pd.read_csv("Dataset/Links.csv")
nodes = pd.read_csv("Dataset/Nodes.csv")

#st.title('Knowledge Graph Analysis')

main_container = st.container()

options_col, chart_col, statistics_col = main_container.columns((1, 4, 1.5))

with options_col:
    # 创建布局
    suspected_entities = st.columns(1)
    node_to_investigate = st.columns(1)
    edge_type_choice = st.columns(1)
    node_type_choice = st.columns(1)
    edge_type_ping = st.columns(1)
    # 多选框，选择需要调查的实体
    entities_to_investigate = ['Mar de la Vida OJSC', '979893388',
                               'Oceanfront Oasis Inc Carriers', '8327']
    # 多选框，选择需要调查的节点
    eti_choice = st.multiselect("怀疑实体:", entities_to_investigate)
    # 获取唯一节点
    entities = nodes['id'].unique().tolist() + ['all']
    eti2_choice = st.multiselect("选择节点:", entities)
    # 如果用户选择了 'all'，则选择所有节点
    if 'all' in eti2_choice:
        eti2_choice = nodes['id']
    # 将所选节点合并
    eti_choice = list(set(eti2_choice) - set(eti_choice)) + \
        eti_choice  # 添加不在数据选择1中但在选择2中的数据

    edge_types = set(links["type"])
    edge_types.add('all')
    # 设置默认选择为'all'
    edge_type_choice = st.multiselect("边类型:", edge_types, default=['all'])

    node_types = set(nodes["type"])
    node_types.add('all')
    # 设置默认选择为'all'
    node_type_choice = st.multiselect("节点类型:", node_types, default=['all'])

    # 设置默认选择为'all'
    # edge_type_ping = st.multiselect("高亮边类型:", edge_types, default=['all'])
    edge_type_ping = st.selectbox("高亮边类型: ", edge_types, index=4)

    st.divider()  # 分割线

    # 滑动条，用于设置权重阈值
    conf_threshold = st.slider(
        'Weight threshold', min_value=0.0000, max_value=1.0, value=0.0000, step=0.0001)


with chart_col:
    # ----------------------------------- Pyvis 设置 -----------------------------------
    # 创建Pyvis网络
    net = Network(notebook=True,  directed=True, height=str(HEIGHT)+"px",
                  width="100%", filter_menu=False, select_menu=False, cdn_resources='remote')

    net.force_atlas_2based(gravity=-10, central_gravity=0.001,
                           spring_length=200, spring_strength=0.01,
                           damping=2, overlap=0)
# ----------------------------------- Pyvis 设置 -----------------------------------


# ----------------------------------- 主要图形逻辑 -----------------------------------

    # 利用NetworkX库创建多重有向图
    graph_type = nx.MultiDiGraph()
    # 注意这里的修改，已将 edge_key 与 edge_attr 调整为正确的用法
    graph = nx.from_pandas_edgelist(
        links, 'source', 'target', edge_attr=True, create_using=graph_type)

    nodes_of_interest = set(eti_choice)
    source_list = []
    target_list = []
    edge_type_list = []

    # 查找与感兴趣实体连接的所有节点
    for entity in eti_choice:
        # 查找指向该实体的节点 (入度)
        for predecessor in graph.predecessors(entity):
            edge_data = graph.get_edge_data(predecessor, entity)
            pred_type = nodes.loc[nodes['id'] == predecessor, 'type'].values[0]
            if edge_data:
                for _, edge_values in edge_data.items():
                    edge_type = edge_values["type"]
                    if edge_values['weight'] >= conf_threshold and (edge_type in edge_type_choice or 'all' in edge_type_choice):
                        if 'all' in node_type_choice or pred_type in node_type_choice:
                            source_list.append(predecessor)
                            target_list.append(entity)
                            edge_type_list.append(edge_values['type'])
                            nodes_of_interest.add(predecessor)
                            nodes_of_interest.add(entity)  # 确保实体也被添加

        # 查找该实体指向的节点 (出度)
        for neighbor in graph.successors(entity):
            edge_data = graph.get_edge_data(entity, neighbor)
            neighbor_type = nodes.loc[nodes['id']
                                      == neighbor, 'type'].values[0]
            if edge_data:
                for _, edge_values in edge_data.items():
                    edge_type = edge_values["type"]
                    if edge_values['weight'] >= conf_threshold and (edge_type in edge_type_choice or 'all' in edge_type_choice):
                        if 'all' in node_type_choice or neighbor_type in node_type_choice:
                            source_list.append(entity)
                            target_list.append(neighbor)
                            edge_type_list.append(edge_values['type'])
                            nodes_of_interest.add(neighbor)
                            nodes_of_interest.add(entity)  # 确保实体也被添加

    # 创建包含感兴趣节点的子图
    sub_graph = graph.subgraph(nodes_of_interest)

    # 为所有边设置颜色属性为
    for (u, v, d) in sub_graph.edges(data=True):
        d['color'] = 'grey'
        title = d.get('type', 'Unknown')  # 提取 type 作为 title
        d['title'] = title
        if title in edge_type_ping and 'all' not in edge_type_ping:
            d['color'] = 'red'

    # 将nx图形转换为pyvis图形
    net = Network(notebook=True, directed=True, height=str(HEIGHT) + "px",width="100%", filter_menu=False, select_menu=False, cdn_resources='remote')
    net.from_nx(sub_graph)

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
        if edge['type'] in edge_type_ping and 'all' not in edge_type_ping:
            edge['width'] = 2

    # 使用force atlas布局可以帮助更好地显示箭头
    net.force_atlas_2based(gravity=-10, central_gravity=0.001,
                           spring_length=200, spring_strength=0.01,
                           damping=2, overlap=0)
    # ----------------------------------- 主要图形逻辑 -----------------------------------

    # ----------------------------------- 图形颜色逻辑 -----------------------------------
    node_colors = {
        'Mar de la Vida OJSC': '#b96570',  # 酒红色
        '979893388': '#062d4b',  # 深蓝色
        'Oceanfront Oasis Inc Carriers': '#248cbf',
        '8327': 'purple'
    }

    node_types_to_colors = {
        'company': '#fcf1f0',
        'organization': '#e4a2b8',
        'person': '#df493f',
        'location': '#b0d992',
        'political_organization': '#f9d580',
        'vessel': '#99b9e9',
        'movement': '#af8fd0',
        'event': '#54beaa',
        'Uncategorized': '#eca680'
    }

    for node in net.nodes:
        # 根据在列表中的位置分配颜色
        if node['id'] in node_colors:
            node['color'] = node_colors[node['id']]
        else:  # 所有节点的颜色（除了entities_to_investigate之外的所有节点）
            node_type = nodes.loc[nodes['id'] ==
                                  node['id'], 'type']  # 查询邻居节点的类型
            node['color'] = node_types_to_colors.get(node_type.values[0])
        # 根据节点的邻居数量分配节点的半径
        node['value'] = 5 * math.log(len(sub_graph[node['id']]) + 1)
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

    # ----------------------------------- 保存图形 -----------------------------------
with statistics_col:
    edge_statistics = {}
    node_statistics = {}
    node_set = set()
    for (u, v, d) in sub_graph.edges(data=True):
        if d["type"] not in edge_statistics:
            edge_statistics[d["type"]] = 1
        else:
            edge_statistics[d["type"]] += 1
        node_set.add(d["source_id"])
        node_set.add(d["target_id"])

    for item in node_set:
        node_type = nodes.loc[nodes['id'] == item, 'type'].values[0]
        if node_type not in node_statistics:
            node_statistics[node_type] = 1
        else:
            node_statistics[node_type] += 1

    edge_bar_chart = Bar()
    edge_bar_chart.add_xaxis(list(edge_statistics.keys()))
    edge_bar_chart.add_yaxis("Edge statistics", list(edge_statistics.values()))
    edge_bar_chart.set_global_opts(
        xaxis_opts=opts.AxisOpts(
            axislabel_opts=opts.LabelOpts(rotate=30, interval=0))
    )
    st_pyecharts(edge_bar_chart, height="350px")

    node_bar_chart = Bar()
    node_bar_chart.add_xaxis(list(node_statistics.keys()))
    node_bar_chart.add_yaxis("Nodes statistics", list(node_statistics.values()),color='#43CD80')
    node_bar_chart.set_global_opts(
        xaxis_opts=opts.AxisOpts(
            axislabel_opts=opts.LabelOpts(rotate=30, interval=0))
    )
    st_pyecharts(node_bar_chart, height="350px")
