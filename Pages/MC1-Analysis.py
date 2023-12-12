import streamlit as st
from streamlit_echarts import st_pyecharts
import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Pie
from pyecharts.charts import Graph, Parallel
from pyecharts.commons.utils import JsCode
import numpy as np
import base64

st.set_page_config(layout="wide", page_icon=None,
                   initial_sidebar_state="collapsed", page_title=None)


page = st.sidebar.selectbox("", ["Graph", "Parallel"])

if page == "Graph":
    links_df = pd.read_csv('Dataset/MC1/Links.csv')
    nodes_df = pd.read_csv('Dataset/MC1/Nodes.csv')

    # Create a dictionary that maps node IDs to their types using the Nodes.csv data
    node_types = nodes_df.set_index('id')['type'].to_dict()
    node_neighbor_count = nodes_df.set_index(
        'id')['neighbor_count'].to_dict()  # 节点邻居节点数量

    # Extract unique nodes and link types
    all_nodes = set(links_df['source']).union(set(links_df['target']))
    link_types = links_df['type'].unique()

    # Hardcode the specified node IDs
    special_node_ids = ["Mar de la Vida OJSC", "979893388",
                        "Oceanfront Oasis Inc Carriers", "8327"]

    # Set up columns for layout
    left_column, mid_column, right_column = st.columns([1, 4, 1.5])

    # Sidebar for selecting nodes and link types
    # Assuming 'type' column has the categories
    node_categories = nodes_df['type'].unique()
    # 默认选中所有类别
    selected_categories = set(node_categories)

    # 添加怀疑节点全局变量
    if 'sus_nodes1' not in st.session_state:
        st.session_state['sus_nodes1'] = set()

    if 'last_action' not in st.session_state:
        st.session_state['last_action'] = None

    selected_nodes = []
    with left_column:

        st.subheader("Quick Select Suspect")
        for node_id in special_node_ids:
            if st.checkbox(node_id, key=node_id):
                selected_nodes.append(node_id)

        st.subheader("Search Node By ID")
        node_query = st.text_input("Node ID", key="node_search")
        if node_query:
            selected_nodes.append(node_query)

        conf_threshold = st.slider(
            'Weight threshold', min_value=0.0000, max_value=1.0, value=0.0000, step=0.0001)

        selected_link_types = set()
        st.subheader("Link Type")
        for link_type in link_types:
            if st.checkbox(link_type, key=f"link_type_{link_type}", value=True):
                selected_link_types.add(link_type)

        st.subheader("Node Type")
        for category in node_categories:
            # 使用default=True使复选框默认被选中
            if st.checkbox(category, key=f"category_{category}", value=True):
                selected_categories.add(category)
            else:
                selected_categories.discard(category)  # 如果用户取消选中，则从集合中移除

    # Function to get neighbors
    def get_neighbors(selected_nodes, links_df, selected_link_types, selected_categories):
        neighbors = set()
        for node in selected_nodes:
            # Check if node is in selected categories
            if node_types[node] in selected_categories:
                filtered_df = links_df[(links_df['type'].isin(selected_link_types)) & (
                    links_df['weight'] > conf_threshold)]
                neighbors.update(
                    filtered_df[filtered_df['source'] == node]['target'].tolist())
                neighbors.update(
                    filtered_df[filtered_df['target'] == node]['source'].tolist())
        return neighbors.union(set(selected_nodes))

    # 定义一个函数来计算节点大小，使用对数函数来增加非线性关系
    def calculate_node_size(neighbor_count, base_size):
        if neighbor_count > 0:
            # 使用对数函数来计算节点大小，确保至少为 base_size
            return base_size + np.sqrt(neighbor_count) * 2.5
        else:
            return base_size

    # Define the colors for each node type
    category_colors = {
        "person": "#df493f",
        "political_organization": "#f9d580",
        "organization": "#e4a2b8",
        "event": "#54beaa",
        "company": "#fcf1f0",
        "location": "#b0d992",
        "vessel": "#99b9e9",
        "movement": "#af8fd0",
        "Uncategorized": "#eca680"
    }

    # 将图片转换为base64编码
    def image_to_base64(path):
        with open(path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        return "data:image/png;base64," + encoded_string

    # 使用上面的函数获取图片的base64编码
    image_path = 'Dataset/MC1/3.png'  # 这里替换为您图片的实际路径
    special_node_base64 = image_to_base64(image_path)

    sus_node_image_path='Dataset/MC1/1.png'
    sus_node_base64 = image_to_base64(sus_node_image_path)

    # 中间列
    with mid_column:
        # ---------------绘制有向图-------------
        if selected_nodes and selected_link_types and selected_categories:
            neighbors_set = get_neighbors(
                selected_nodes, links_df, selected_link_types, selected_categories)
            filtered_df = links_df[(links_df['source'].isin(neighbors_set)) & (
                links_df['target'].isin(neighbors_set)) & (links_df['type'].isin(selected_link_types))]

            echarts_nodes = [
                {
                    "name": node,
                    # 使用neighbor_count字典设置节点大小，如果节点ID不在字典中，默认大小为5
                    "symbolSize": calculate_node_size(node_neighbor_count.get(node), 1),
                    "draggable": True,
                    "category": node_types.get(node, "Unknown"),
                    # Set shape to star for special nodes
                    "symbol": 'image://' + special_node_base64 if node in special_node_ids else (
                        'image://' + sus_node_base64 if node in st.session_state['sus_nodes1'] else 'circle'
                    ),
                }
                for node in neighbors_set
            ]

            echarts_links = filtered_df.apply(
                lambda row: {"source": row['source'],
                             "target": row['target'], "value": row['type']}
                if row['weight'] > conf_threshold else None,
                axis=1
            ).dropna().tolist()

            # 定义不同类别的节点样式
            categories = [
                {"name": "person", "itemStyle": {"color": "#df493f"}},
                {"name": "political_organization",
                    "itemStyle": {"color": "#f9d580"}},
                {"name": "organization", "itemStyle": {"color": "#e4a2b8"}},
                {"name": "event", "itemStyle": {"color": "#54beaa"}},
                {"name": "company", "itemStyle": {"color": "#fcf1f0"}},
                {"name": "location", "itemStyle": {"color": "#b0d992"}},
                {"name": "vessel", "itemStyle": {"color": "#99b9e9"}},
                {"name": "movement", "itemStyle": {"color": "#af8fd0"}},
                {"name": "Uncategorized", "itemStyle": {"color": "#eca680"}}
            ]

            graph = Graph()

            graph.add(
                series_name="",  # 系列名称，这里留空
                nodes=echarts_nodes,
                links=echarts_links,
                categories=categories,
                layout="force",  # 使用力导向布局
                symbol_size=10,
                is_roam=True,  # 允许漫游
                is_draggable=True,  # 允许拖动
                is_focusnode=True,  # 聚焦节点
                label_opts=opts.LabelOpts(
                    position="right", color="black"),  # 节点标签选项
                edge_symbol=["none", "arrow"],  # 边的符号，这里设置为无和箭头
                edge_symbol_size=10,
                linestyle_opts=opts.LineStyleOpts(
                    width=2, curve=0.1, opacity=0.9),  # 线条样式
                itemstyle_opts=opts.ItemStyleOpts(
                    border_width=0, border_color="#fff"),  # 项样式
                # 下面是针对力导向图的特定参数
                repulsion=50,  # 节点之间的斥力因子
                gravity=0.2,  # 重力因子
                edge_length=30,  # 边的长度
                friction=0.6,  # 摩擦力
                is_layout_animation=True  # 是否启用布局动画
            )

            graph.set_global_opts(
                title_opts=opts.TitleOpts(title=""),  # 设置标题
                legend_opts=opts.LegendOpts(
                    selected_mode=True,
                ),  # 设置图例的选择模式
                tooltip_opts=opts.TooltipOpts(),  # 设置工具提示
                toolbox_opts=opts.ToolboxOpts(      # 设置工具箱
                    pos_left="80%",  # 调整为适当的百分比以放置在右侧
                    pos_top="bottom",  # 设置为 'bottom' 使其出现在底部
                ),
            )

            graph.set_series_opts(
                label_opts=opts.LabelOpts(
                    is_show=True,  # 节点上的id标签
                    position='right',  # 将标签位置设置在节点的右侧
                    color='black',  # 将标签颜色设置为黑色
                )
            )

            # 设置点击事件的JavaScript函数
            click_event_js = "function(params) {return params.data;}"

            # 渲染有向图并设置点击事件
            result = st_pyecharts(graph,
                                  events={"click": click_event_js},
                                  width="100%",
                                  height=1000)

            if result:
                # 更新点击的节点ID
                st.session_state['clicked_node'] = result["name"]
                st.session_state['last_action'] = 'click'

            # ---------------绘制饼图-------------
            # 创建饼图对象
            pie1 = Pie()
            pie2 = Pie()

            # 第一个饼图
            # Calculate the count of each link type in the filtered graph
            neighbors_set = get_neighbors(
                selected_nodes, links_df, selected_link_types, selected_categories)
            filtered_df = links_df[((links_df['source'].isin(selected_nodes)) | (
                links_df['target'].isin(selected_nodes))) & (links_df['type'].isin(selected_link_types))]
            link_type_counts = filtered_df['type'].value_counts().reset_index()
            link_type_counts.columns = ['type', 'count']

            # Calculate in-degree and out-degree for each link type
            in_degree_counts = links_df[links_df['target'].isin(
                selected_nodes)]['type'].value_counts().reset_index()
            out_degree_counts = links_df[links_df['source'].isin(
                selected_nodes)]['type'].value_counts().reset_index()

            # Transform the value counts into the format needed for ECharts
            def transform_counts_to_data(counts):
                return [{"value": row['count'], "name": row['type']} for index, row in counts.iterrows()]

            all_degree_data = transform_counts_to_data(link_type_counts)
            in_degree_data = transform_counts_to_data(in_degree_counts)
            out_degree_data = transform_counts_to_data(out_degree_counts)

            # Sort the data by the 'name' key using sorted function
            all_degree_data = sorted(
                all_degree_data, key=lambda x: x['name'].lower())
            in_degree_data = sorted(
                in_degree_data, key=lambda x: x['name'].lower())
            out_degree_data = sorted(
                out_degree_data, key=lambda x: x['name'].lower())

            all_degree_data = [(item['name'], item['value'])
                               for item in all_degree_data]
            in_degree_data = [(item['name'], item['value'])
                              for item in in_degree_data]
            out_degree_data = [(item['name'], item['value'])
                               for item in out_degree_data]

            # 检查数据集是否为空，如果不为空则添加到饼图中

            def safe_add_pie_series(pie, series_name, data_pair, radius, center, label_opts):
                if data_pair:  # 如果数据对非空
                    pie.add(
                        series_name=series_name,
                        data_pair=data_pair,
                        radius=radius,
                        center=center,
                        label_opts=label_opts,
                    )

            # 为饼图添加多个系列，确保不为空
            safe_add_pie_series(
                pie1, '', all_degree_data if all_degree_data else [], [
                    '0%', '30%'], ["40%", "60%"], opts.LabelOpts(is_show=False)
            )

            safe_add_pie_series(
                pie1, '', in_degree_data if in_degree_data else [], [
                    '40%', '55%'], ["40%", "60%"], opts.LabelOpts(is_show=False)
            )

            safe_add_pie_series(
                pie1, '', out_degree_data if out_degree_data else [], [
                    '65%', '80%'], ["40%", "60%"], opts.LabelOpts(is_show=False)
            )

            graphic_opts = [
                opts.GraphicText(
                    graphic_item=opts.GraphicItem(
                        left="47%",  # 水平居中对齐饼图中心
                        top="45%",  # 假设这个位置在内层饼图的中心以上
                        z=100,
                    ),
                    graphic_textstyle_opts=opts.GraphicTextStyleOpts(
                        text="in_degree",
                        font="bold 14px Arial",
                        graphic_basicstyle_opts=opts.GraphicBasicStyleOpts(
                            fill="#000")
                    ),
                ),
                opts.GraphicText(
                    graphic_item=opts.GraphicItem(
                        left="60%",  # 水平居中对齐饼图中心
                        top="55%",  # 假设这个位置在内层饼图的中心以下
                        z=100,
                    ),
                    graphic_textstyle_opts=opts.GraphicTextStyleOpts(
                        text="out_degree",
                        font="bold 14px Arial",
                        graphic_basicstyle_opts=opts.GraphicBasicStyleOpts(
                            fill="#000")
                    ),
                )
            ]

            # 设置饼图的全局配置
            pie1.set_global_opts(
                tooltip_opts=opts.TooltipOpts(
                    trigger="item",
                    # 鼠标悬浮的提示框内容
                    formatter=JsCode(
                        "function(params){"
                        "    var colorSpan = '<span style=\"display:inline-block;margin-right:4px;border-radius:10px;width:10px;height:10px;background-color:' + params.color + ';\"></span>';"
                        "    return colorSpan + params.name + ': ' + params.value + ' (' + params.percent + '%)';"
                        "}"
                    )
                ),
                # 鼠标悬浮时的提示框配置
                legend_opts=opts.LegendOpts(
                    orient="horizontal",
                    pos_left="left"),
                # 图例配置，设置为水平方向并靠左显示
                graphic_opts=graphic_opts,  # 在这里设置自定义文本标签的配置
            )

            # 第二个饼图
            # Calculate the count of each node type in the filtered graph
            node_type_counts = nodes_df[nodes_df['id'].isin(
                neighbors_set)]['type'].value_counts().reset_index()
            node_type_counts.columns = ['type', 'count']

            # Prepare data for ECharts pie chart based on node statistics
            node_pie_data = [
                {
                    "value": count,
                    "name": node_type,
                    # Default to black if not found
                    "itemStyle": {"color": category_colors.get(node_type, "#000000")}
                }
                for node_type, count in zip(node_type_counts['type'], node_type_counts['count'])
            ]

            # 设置饼图的全局配置
            pie2.set_global_opts(
                tooltip_opts=opts.TooltipOpts(
                    trigger="item",
                    # 鼠标悬浮的提示框内容
                    formatter=JsCode(
                        "function(params){"
                        "    var colorSpan = '<span style=\"display:inline-block;margin-right:4px;border-radius:10px;width:10px;height:10px;background-color:' + params.color + ';\"></span>';"
                        "    return colorSpan + params.name + ': ' + params.value + ' (' + params.percent + '%)';"
                        "}"
                    )
                ),
                legend_opts=opts.LegendOpts(
                    orient="horizontal",  # 图例水平放置
                    pos_left="left",  # 图例垂直放置在左侧
                    background_color="transparent"  # Set the legend background color to transparent
                )
            )

            color_series = [item['itemStyle']['color']
                            for item in node_pie_data]

            # 添加数据系列
            pie2.add(
                series_name="",  # 系列名称，如果只有一个系列可以为空
                data_pair=[(item['name'], item['value'])
                           for item in node_pie_data],  # 数据对，必须是(name, value)格式的序列
                radius="80%",  # 饼图的半径
                center=["40%", "60%"],  # 饼图的中心（圆心）位置
                label_opts=opts.LabelOpts(is_show=False),  # 标签配置，这里设置为不显示标签
            )

            # 设置颜色
            pie2.set_colors(color_series)

            # Render pie charts side by side
            left_pie, right_pie = st.columns(2)

            with left_pie:
                st.subheader("edge Statistics")
                st_pyecharts(pie1, height="400px")

            with right_pie:
                st.subheader("Node Statistics")
                st_pyecharts(pie2, height="400px")

            # ---------用户点击图表交互---------
    with right_column:
        # 定义变量保存当前点击的节点ID
        current_node_id = None

        # 筛选框
        st.subheader("Suspect Set")
        # 这里可以添加你需要的筛选框或其他控件
        selected_sus_node = st.selectbox("Select the suspected node", list(
            st.session_state['sus_nodes1']), index=0, key='suspect_select')

        if selected_sus_node:
            if (selected_sus_node != st.session_state.get('selected_node')) or (st.session_state.get('last_action') != 'click'):
                # 更新选择的节点ID，并将操作设置为“select”
                st.session_state['selected_node'] = selected_sus_node
                st.session_state['last_action'] = 'select'

        # 显示节点信息
        if st.session_state.get('last_action') == 'click':
            current_node_id = st.session_state.get('clicked_node')
        else:
            current_node_id = st.session_state.get('selected_node')

        if current_node_id:
            # 读取节点信息
            node_info_df = pd.read_csv(
                'Dataset/MC1/community_node_information.csv')
            # 检索节点信息
            node_info = node_info_df[node_info_df['Node']
                                     == current_node_id]  # 假设CSV有一个'Node'列

            # 在右侧列显示节点信息
            # 创建一个选择框让用户选择信息类型
            # 创建单选按钮
            info_type = st.radio(
                "",
                ('ID', 'Statistics', 'Community Information')
            )

            # 添加横线
            st.markdown("---")

            # 定义 CSS 样式
            my_font_style = """
            <style>
            .my-font {
                font-family: Arial;
                color: skyblue;
                font-size: 20px;
            }
            <yle>
            """

            # 应用 CSS 样式
            st.markdown(my_font_style, unsafe_allow_html=True)

            # 使用自定义样式显示文本
            # st.markdown('<p class="my-font">这是自定义字体样式的文本</p>', unsafe_allow_html=True)

            if info_type == 'ID':
                # 显示第2到9列
                for col in node_info.columns[1:8]:  # Python 列索引从0开始
                    # st.text(f"{col}: {node_info.iloc[0][col]}")
                    st.markdown(
                        f'<p class="my-font">"{col}: {node_info.iloc[0][col]}"</p>', unsafe_allow_html=True)
            elif info_type == 'Statistics':
                # 显示第10到21列
                for col in node_info.columns[8:21]:
                    st.text(f"{col}: {node_info.iloc[0][col]}")
            elif info_type == 'Community Information':
                # 显示第1列和第22列
                st.text(f"{node_info.columns[0]}: {node_info.iloc[0][0]}")
                st.text(f"{node_info.columns[21]}: {node_info.iloc[0][21]}")

        # 添加另一个分隔符
        st.markdown("---")

        # 创建两列来放置按钮
        col1, col2 = st.columns(2)
        with col1:
            def handle_add_set():
                st.session_state['sus_nodes1'].add(current_node_id)

            st.button('Add to Suspect Set', on_click=handle_add_set)

        with col2:
            def handle_remove():
                st.session_state['sus_nodes1'].discard(selected_sus_node)

            st.button('Remove', on_click=handle_remove)



#----------------平行坐标-----------------
elif page == "Parallel":
    # Streamlit application layout
    st.title("Community Visualization")

    # Controls for community selection and chart type, placed at the top
    community_number = st.selectbox("Select a Community Number", range(16))
    chart_type = st.radio("Select Chart Type", ("Community Graph", "Parallel"))

    # Load data
    node_data = pd.read_csv(
        "Dataset/MC1/Parallel_coordinates/community_node_stats.csv")
    edge_data = pd.read_csv("Dataset/MC1/Links.csv")
    parallel_data = pd.read_csv(
        "Dataset/MC1/Parallel_coordinates/community_node_stats.csv")
    parallel_ave_data = pd.read_csv(
        "Dataset/MC1/Parallel_coordinates/community_stats.csv")

    # Suspected nodes list
    suspected_nodes = ["Mar de la Vida OJSC", "979893388",
                       "Oceanfront Oasis Inc Carriers", "8327"]

    # 将图片转换为base64编码
    def image_to_base64(path):
        with open(path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        return "data:image/png;base64," + encoded_string

    # 使用上面的函数获取图片的base64编码
    image_path = 'Dataset/MC1/3.png'  # 这里替换为您图片的实际路径
    special_node_base64 = image_to_base64(image_path)

    # Filter nodes and edges based on the selected community
    filtered_nodes = node_data[node_data["Community"] == community_number]
    filtered_edges = edge_data[edge_data["source"].isin(
        filtered_nodes["id"]) & edge_data["target"].isin(filtered_nodes["id"])]
    filtered_parallel = parallel_data[parallel_data.iloc[:, 0]
                                      == community_number]

    # 绘制图
    def display_graph(filtered_nodes, filtered_edges):
        # Define categories and their respective colors
        categories_list = [
            "person", "political_organization", "organization", "event", "company",
            "location", "vessel", "movement", "Uncategorized"
        ]
        colors = ["#df493f", "#f9d580", "#e4a2b8", "#54beaa",
                  "#fcf1f0", "#b0d992", "#99b9e9", "#af8fd0", "#eca680"]
        categories = [{"name": category, "itemStyle": {"color": color}}
                      for category, color in zip(categories_list, colors)]

        # Create a mapping from type to category index
        type_to_category = {type_: index for index,
                            type_ in enumerate(categories_list)}

        # Prepare graph data
        nodes = []
        for _, node in filtered_nodes.iterrows():
            category_index = type_to_category.get(
                node["type"], len(categories_list) - 1)
            node_color = categories[category_index]["itemStyle"]["color"]
            # Check if the node name is in suspected_nodes
            is_suspected = node["id"] in suspected_nodes
            nodes.append({
                "name": str(node["id"]),
                "symbolSize": 30,
                "category": category_index,
                "itemStyle": {"color": node_color},
                "label": {"show": False},   # Set label color to black
                "symbol": 'image://' + special_node_base64 if is_suspected else 'circle',
            })

        links = [{"source": str(source), "target": str(target)} for source, target in zip(
            filtered_edges["source"], filtered_edges["target"])]

        # Create and display a graph
        g = Graph(init_opts=opts.InitOpts(width="100%", height="1000px"))
        g.add("", nodes, links, repulsion=5000, categories=categories)
        g.set_global_opts(title_opts=opts.TitleOpts(title="Community Graph"))
        st_pyecharts(g, width="100%", height=800)

    # 绘制平行坐标
    def display_parallel(filtered_parallel, suspected_nodes, parallel_ave_data, community_number):
        # Convert suspected_nodes to a set for faster lookup
        suspected_nodes_set = set(suspected_nodes)

        # Prepare parallel data
        schema = [opts.ParallelAxisOpts(dim=i, name=col) for i, col in enumerate(
            filtered_parallel.columns[4:])]
        ids = filtered_parallel["id"].tolist()  # Extract ids for performance
        suspected_data = []
        normal_data = []

        # Add data for each node with their IDs and category as part of the name
        for i, row in enumerate(filtered_parallel.itertuples()):
            is_suspected = ids[i] in suspected_nodes_set
            category = "Suspected" if is_suspected else "Normal"
            data_point = {
                "value": list(row)[5:],  # Skip index and first 4 columns
                "name": f"{category} - ID: {ids[i]}"  # Combine category and ID
            }
            if is_suspected:
                suspected_data.append(data_point)
            else:
                normal_data.append(data_point)

        # Create and display a parallel chart
        parallel = Parallel(init_opts=opts.InitOpts(
            width="100%", height="600px"))
        parallel.add_schema(schema)

        # Set tooltip formatting to show both category and ID
        tooltip_formatter = opts.TooltipOpts(
            formatter=lambda params: params.name)

        # When adding data to the parallel chart, include the formatted tooltip
        parallel.add("Normal", normal_data, linestyle_opts=opts.LineStyleOpts(
            color='#ADD8E6'), tooltip_opts=tooltip_formatter)
        parallel.add("Suspected", suspected_data, linestyle_opts=opts.LineStyleOpts(
            color='red', width=3), tooltip_opts=tooltip_formatter)
        # Add average data for the selected community
        avg_data = parallel_ave_data[parallel_ave_data["Community"]
                                     == community_number]
        if not avg_data.empty:
            # Skip first three columns
            avg_values = avg_data.iloc[0, 3:].tolist()
            parallel.add("Average", [{"value": avg_values}], linestyle_opts=opts.LineStyleOpts(
                color="blue", width=3))

        parallel.set_global_opts(
            title_opts=opts.TitleOpts(title="Community Parallel Coordinates"),
            legend_opts=opts.LegendOpts()  # Add legend options
        )
        st_pyecharts(parallel)

    # Depending on the chart type, display the respective chart
    if chart_type == "Community Graph":
        display_graph(filtered_nodes, filtered_edges)
    elif chart_type == "Parallel":
        display_parallel(filtered_parallel, suspected_nodes,
                         parallel_ave_data, community_number)
