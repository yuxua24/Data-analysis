import streamlit as st
from streamlit_echarts import st_pyecharts
from pyecharts import options as opts
from pyecharts.charts import HeatMap
import pandas as pd
from pyecharts.commons.utils import JsCode
from pyecharts.charts import Graph
from pyecharts.charts import Bar
from pyecharts.options import LabelOpts
from pyecharts.charts import Grid
import numpy as np
import json


st.set_page_config(layout="wide", page_icon=None,
                   initial_sidebar_state="collapsed", page_title=None)

hide_st_style = """
            <style>
            /* Removes padding, margin and set full height to the main content area */
            .main .block-container { 
                padding-top: 0rem; 
                padding-right: 0rem;
                padding-left: 1rem;
                padding-bottom: 0rem;
                margin: 0;
            }
            /* Additional custom styles can be added here */
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)


# 页面比例
page_ratio = st.slider('Page Ratio', min_value=0.0000, max_value=1.0,
                       value=0.35, step=0.0001, label_visibility='hidden')


# 如果不存在 'all_chosen_nodes'，在 session state 中初始化它
if 'all_chosen_nodes' not in st.session_state:
    st.session_state.all_chosen_nodes = []

if 'clear_signal' not in st.session_state:
    st.session_state.clear_signal = False


# 初始化 session state 变量
if 'click_result' not in st.session_state:
    st.session_state.click_result = None


# 确保 graph_node 和 graph_link 在 session_state 中持久化
if 'graph_node' not in st.session_state:
    st.session_state.graph_node = []
if 'graph_link' not in st.session_state:
    st.session_state.graph_link = []


# 在 Streamlit 中创建或更新 session state 变量以跟踪选中的国家
if 'selected_x' not in st.session_state:
    st.session_state.selected_x = None


company_type = pd.read_csv('Dataset/MC3/heat_map/country-company_type-new.csv')
company_label = pd.read_csv('Dataset/MC3/heat_map/country-company_label.csv')
country_category = pd.read_csv(
    'Dataset/MC3/heat_map/country-category_counts-new.csv')
size_revenue = pd.read_csv('Dataset/MC3/heat_map/size-revenue.csv')
country_company_revenue = pd.read_csv(
    'Dataset/MC3/heat_map/country-company_revenue.csv')
product_service_size = pd.read_csv(
    'Dataset/MC3/heat_map/Product_Service-Size.csv')
product_service_revenue = pd.read_csv(
    'Dataset/MC3/heat_map/Product_Service-revenue.csv')

nodes = pd.read_csv('Dataset/MC3/nodes.csv')
links = pd.read_csv('Dataset/MC3/links.csv')

country_count=pd.read_csv("Dataset/MC3/bar/Country_count.csv")
label_count=pd.read_csv("Dataset/MC3/bar/Label_count.csv")
company_revenue_count=pd.read_csv("Dataset/MC3/bar/company_revenue_count.csv")
person_revenue_count=pd.read_csv("Dataset/MC3/bar/person_revenue_count.csv")
company_size_count=pd.read_csv("Dataset/MC3/bar/company_size_count.csv")

# 优化后的数据处理函数
def process_heatmap_data(heatmap_choice):
    if heatmap_choice == 'country-company_type':
        data_df = company_type
    elif heatmap_choice == 'country-company_label':
        data_df = company_label
    elif heatmap_choice == 'size-revenue':
        data_df = size_revenue
    elif heatmap_choice == 'country-company_revenue':
        data_df = country_company_revenue
    elif heatmap_choice == 'product_service-size':
        data_df = product_service_size
    elif heatmap_choice == 'product_service-revenue':
        data_df = product_service_revenue
    else:
        data_df = country_category

    data = [
        [col_index - 1, row_index, row[col_index]]
        for row_index, row in data_df.iterrows()
        for col_index in range(1, len(row))
    ]
    min_value = min(value for _, _, value in data)
    max_value = max(value for _, _, value in data)

    return data_df.keys()[1:], data_df.iloc[:, 0], data, data_df, min_value, max_value


# 根据用户的选择来处理数据
def process_data(data, log_scale):
    if log_scale:
        # Apply a logarithmic transformation to the third element of each list
        processed_data = [[x[0], x[1], np.log2(x[2]+1)] for x in data]
        # Extract the third element from each sub-list for min and max calculation
        values = [x[2] for x in processed_data]
        # Calculate new min and max values
        min_value = min(values)
        max_value = max(values)
    else:
        processed_data = data
        # Extract the third element from each sub-list for min and max calculation
        values = [x[2] for x in data]
        # Use original min and max values
        min_value = min(values)
        max_value = max(values)
    return processed_data, min_value, max_value


main_container = st.container()
options_col, chart_col = main_container.columns((page_ratio, 1-page_ratio))

graph_node = []
graph_link = []


with options_col:
    heatmap_type = ['country-company_type',
                    'country-company_label',
                    'country-category_counts',
                    'country-company_revenue',
                    'size-revenue',
                    'product_service-size',
                    'product_service-revenue']
    heatmap_choice = st.selectbox("选择热力图类型:", heatmap_type)

    xaxis_labels, yaxis_labels, data, data_df, min_value, max_value = process_heatmap_data(
        heatmap_choice)

    col1, mid, col2 = st.columns(3)

    with col1:
        # 如果点击了“清除选中节点”按钮
        if st.button('Clear Selection'):
            st.session_state.all_chosen_nodes.clear()
            st.session_state.clear_signal = True  # 设置标志，指示需要忽略点击事件

    with col2:
        # 添加一个勾选框，用户可以选择是否应用对数尺度
        log_scale = st.checkbox('Log Color Scale')

    processed_data, min_value, max_value = process_data(data, log_scale)

    # 创建热力图
    heatmap = (
        HeatMap()
        .add_xaxis(list(xaxis_labels))
        .add_yaxis(
            series_name=heatmap_choice,
            yaxis_data=list(yaxis_labels),
            value=processed_data,
            label_opts=opts.LabelOpts(is_show=False, position="inside"),
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title="HeatMap"),
            legend_opts=opts.LegendOpts(is_show=False),  # 关闭图例显示
            # 标签样式
            tooltip_opts=opts.TooltipOpts(
                is_show=True,  # 是否显示提示框组件，包括提示框浮层和 axisPointer。
                trigger="item",  # 触发类型。'item' 表示数据项图形触发。
                position="inside",
                axis_pointer_type='cross',  # 使用十字准线指示器
                background_color="rgba(50,50,50,0.7)",  # 提示框浮层的背景颜色。
                border_color="#333",  # 提示框浮层的边框颜色。
                border_width=0,  # 提示框浮层的边框宽。
                textstyle_opts=opts.TextStyleOpts(color="#fff"),  # 提示框浮层的文本样式。
                formatter=JsCode("function(params){return params.value[2] + ' nodes';}") if not log_scale else (
                    JsCode(
                        "function(params){return (2 ** params.value[2]-1).toFixed(0)  + ' nodes';}")
                )
            ),
            axispointer_opts=opts.AxisPointerOpts(
                is_show=True,
                type_="none",  # 'line' | 'shadow' | 'none'

            ),
            xaxis_opts=opts.AxisOpts(
                axislabel_opts=opts.LabelOpts(font_size=5),
                position="bottom",
            ),
            yaxis_opts=opts.AxisOpts(
                axislabel_opts=opts.LabelOpts(font_size=10, is_show=True),
                name_gap=100,  # 增加轴名称和轴线之间的距离
                name_textstyle_opts=opts.TextStyleOpts(
                    font_size=10),  # 可以调整y轴名称的字体大小
            ),
            visualmap_opts=opts.VisualMapOpts(
                is_show=False,  # 隐藏视觉映射控件
                min_=min_value,
                max_=max_value,
                is_calculable=True,
                orient="horizontal",
                pos_left="center",
                range_color=["#ffffff", "#000080"]  # 从白色到深蓝色
            ),
        )
    )

    # 计算宽度和高度
    num_x_labels = len(xaxis_labels)
    num_y_labels = len(yaxis_labels)

    # 假设每个单元格的大小为25像素，您可以根据需要调整
    cell_size = 25
    width = cell_size * num_x_labels
    height = cell_size * num_y_labels

    # 设置点击事件的JavaScript函数
    click_event_js = "function(params) {return params.data;}"

    # 渲染热力图并设置点击事件
    node_chosen = st_pyecharts(
        heatmap,
        events={"click": click_event_js},
        width=f"{width}px",
        height=f"{height}px"
    )

    # 当热力图被点击时，添加新节点到 session state
    if node_chosen and node_chosen not in st.session_state.all_chosen_nodes and st.session_state.clear_signal is False:
        st.session_state.all_chosen_nodes.append(node_chosen)

    # 如果清除信号被设置，则重置该信号
    if st.session_state.clear_signal:
        st.session_state.clear_signal = False

    st.write(st.session_state.all_chosen_nodes)

    with mid:
        # 如果点击了“添加到图表”按钮
        if st.button('Add to Graph'):
            # temp_chosen_nodes = st.session_state.all_chosen_nodes.copy()
            # st.session_state.all_chosen_nodes = []
            # st.session_state.clear_signal = True  # 设置标志，指示需要忽略点击事件

            # 遍历 node_chosen 列表
            for item in st.session_state.all_chosen_nodes:
                if isinstance(item, list) and len(item) == 3:
                    col_idx, row_idx, number = item
                    if number != 0:
                        selected_country = data_df.iloc[row_idx, 0]  # 国家信息在第0列
                        # +1 因为我们跳过了第一列，它通常是索引列
                        selected_company_type = data_df.columns[col_idx + 1]

                        filtered_df = nodes[(nodes['country'] == selected_country) & (
                            nodes['company_type'] == selected_company_type)]
                        st.session_state.graph_node.extend(
                            filtered_df['id'].tolist())

            # 去除重复的节点ID
            st.session_state.graph_node = list(
                set(st.session_state.graph_node))

            # # 打印结果将
st.write("graph_node:", st.session_state.graph_node)


# 定义类型到颜色的映射
type_color_mapping = {
    'Beneficial Owner': '#9E4A5F',   # 请用实际的颜色代码替换 'color1'，例如 '#ff0000'
    'Company': '#494564',            # 请用实际的颜色代码替换 'color2'，例如 '#00ff00'
    'Company Contacts': '#bad077',   # 请用实际的颜色代码替换 'color3'，例如 '#0000ff'
}


# 创建节点类型列表
node_categories = [
    {"name": "Beneficial Owner", "itemStyle": {"color": "#9E4A5F"}},
    {"name": "Company", "itemStyle": {"color": "#494564"}},
    {"name": "Company Contacts", "itemStyle": {"color": "#bad077"}}
]


# 使用 chart_col 作为父容器来创建两个子容器
upper_chart_container = chart_col.container()
mid_chart_container = chart_col.container()
lower_chart_container = chart_col.container()

with upper_chart_container:
    # 分为左右两部分，左边展示图，右边展示信息
    left_part, right_part = upper_chart_container.columns([12, 1])

    with left_part:
        # 筛选出与 graph_node 相关的边
        filtered_links = links[links['source'].isin(
            st.session_state.graph_node) & links['target'].isin(st.session_state.graph_node)]

        # 准备节点和边的数据
        # 准备节点数据，为每个类型的节点设置不同的颜色
        nodes_data = [
            {
                "name": str(node['id']),
                "details": ','.join(f"{key}  :  {str(node[key])}" for key in node.keys()),
                "symbolSize": 40,
                "draggable": "True",  # 确保节点是可拖拽的
                "category": node['type'],  # 假设 nodes DataFrame 有一个 'type' 列
                "itemStyle": {"color": type_color_mapping.get(node['type'], 'default_color')}
            }
            for index, node in nodes.iterrows() if node['id'] in st.session_state.graph_node
        ]
        links_data = [{"source": str(row['source']),
                       "target": str(row['target'])} for index, row in filtered_links.iterrows()]

        # 创建图表
        graph = Graph()
        graph.add("",
                  nodes_data,
                  links_data,
                  categories=node_categories,  # 添加 categories
                  repulsion=4000)
        graph.set_global_opts(
            title_opts=opts.TitleOpts(title="Directed Graph"))

        # 标签
        graph.set_series_opts(
            label_opts=LabelOpts(
                is_show=True,  # 显示标签
                position="right",  # 标签位置
                font_size=14,  # 字体大小
                color="auto",  # 标签字体颜色，'auto'为自动颜色
                # 使用节点的name属性作为标签
                formatter=JsCode("function(data){return data.data.name;}")
            )
        )

        # 设置鼠标悬浮时的提示框
        graph.set_global_opts(
            tooltip_opts=opts.TooltipOpts(
                is_show=True,
                formatter=JsCode("""
                    function(data) {
                        return data.data.details.replace(/,/g, '<br/>');
                    }
        """)
            )
        )

        # 设置点击事件的JavaScript函数
        click_event_js = "function(params) {return params.data;}"

        # 渲染有向图并设置点击事件
        result = st_pyecharts(graph,
                              events={"click": click_event_js},
                              height="600px",
                              width="100%")

        # 检查点击事件的结果
        if result:
            st.session_state.click_result = result

        # 在右边的部分显示点击的节点信息
    with right_part:
        if st.button('Clear Graph'):
            pass  # 清除图所有节点


with mid_chart_container:
    left, mid, right = mid_chart_container.columns([2, 1, 1])

with left:
    Histogram_type = ['Country', 'Label',
                      'Personal Revenue', 'Company Revenue','company size']
    bar_choice = st.selectbox("选择柱状图类型:", Histogram_type)

with mid:
    hide_missing = st.checkbox('Hide Missing')

with right:
    # 添加一个勾选框，用户可以选择是否应用对数尺度
    log_scale2 = st.checkbox('Log Color Scale ')


def process_bar_data2(bar_choice, hide_missing):
    if bar_choice == 'Country':
        bar_data = country_count
    elif bar_choice == 'Company Revenue':
        bar_data = company_revenue_count
    elif bar_choice == 'Personal Revenue':
        bar_data = person_revenue_count
    elif bar_choice == 'company size':
        bar_data = company_size_count
    else:
        bar_data = label_count

    # 如果勾选了“Hide Missing”，过滤掉标记为“missing”的数据
    if hide_missing:
        bar_data = bar_data[bar_data[bar_data.columns[0]] != 'missing']
    return bar_data


with lower_chart_container:

    bar_data = process_bar_data2(bar_choice, hide_missing)
    selectes_type = bar_data.columns[0]

    # 根据log_scale2复选框的状态选择是否取对数
    if log_scale2:
        counts = np.log2(bar_data['count']+1).tolist()
    else:
        counts = bar_data['count'].tolist()

    if st.session_state.click_result:
        print("====")
        clicked_node_id = st.session_state.click_result['name']
        # 获取点击的节点对应的国家名称
        selected_country = nodes[nodes['id'] ==
                                 clicked_node_id][selectes_type].values[0]
        st.session_state.selected_x = selected_country
        print(st.session_state.selected_x)
        bar_item_colors = ['#A01D14' if country ==
                           st.session_state.selected_x else '#2E5276' for country in bar_data[selectes_type].tolist()]
    else:
        bar_item_colors = ['#2E5276'] * len(bar_data[selectes_type])

    # 将 y_data 转换为包含样式的字典列表
    y_data_with_style = [{"value": y, "itemStyle": {"color": color}}
                         for y, color in zip(counts, bar_item_colors)]

    # 创建直方图
    bar = Bar()
    bar.add_xaxis(bar_data[selectes_type].tolist())
    bar.add_yaxis("count", y_data_with_style,
                  label_opts=opts.LabelOpts(is_show=False))
    bar.set_global_opts(
        # title_opts=opts.TitleOpts(title="Country Count Histogram"),
        legend_opts=opts.LegendOpts(is_show=False),
        yaxis_opts=opts.AxisOpts(name="number"),
        xaxis_opts=opts.AxisOpts(name=selectes_type),  # x轴上标签旋转
        tooltip_opts=opts.TooltipOpts(
            is_show=True,
            trigger="axis",  # 当鼠标悬停在轴的时候显示
            axis_pointer_type="cross",  # 十字线指针
            formatter=(
                "{b} <br/> Count: {c}" if not log_scale2 else
                JsCode(
                    "function(params) {return params[0].axisValueLabel + ' <br/> Count: ' + (2 ** (params[0].data.value) - 1).toFixed(0);}")
            )
        ),
    )

    # 创建 Grid 实例
    grid = Grid()

    # 将柱状图 (bar) 添加到 Grid 中，并设置 grid 的布局选项
    # 此处设置了 left 边距为 10%，可以根据需要调整
    grid.add(bar, grid_opts=opts.GridOpts(pos_left="5%"))

    # 在 Streamlit 中渲染直方图
    st_pyecharts(bar, height="400px", width="100%")
