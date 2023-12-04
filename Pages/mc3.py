import streamlit as st
from streamlit_echarts import st_pyecharts
from pyecharts import options as opts
from pyecharts.charts import HeatMap
import pandas as pd

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
                       value=0.5, step=0.0001, label_visibility='hidden')


# 如果不存在 'all_chosen_nodes'，在 session state 中初始化它
if 'all_chosen_nodes' not in st.session_state:
    st.session_state.all_chosen_nodes = []

if 'clear_signal' not in st.session_state:
    st.session_state.clear_signal = False

company_type = pd.read_csv('Dataset/MC3/country-company_type.csv')
company_lable = pd.read_csv('Dataset/MC3/country-company_lable.csv')
company_revenue = pd.read_csv('Dataset/MC3/country-company_revenue.csv')
related2seafood = pd.read_csv('Dataset/MC3/country-company_related2seafood.csv')

nodes=pd.read_csv('Dataset/MC3/nodes.csv')
links=('Dataset/MC3/links.csv')

# 优化后的数据处理函数
def process_heatmap_data(heatmap_choice):
    if heatmap_choice == 'country-company_type':
        data_df = company_type
    elif heatmap_choice == 'country-company_lable':
        data_df = company_lable
    elif heatmap_choice == 'country-company_revenue':
        data_df = company_revenue
    else:
        data_df = related2seafood

    data = [
        [col_index - 1, row_index, row[col_index]]
        for row_index, row in data_df.iterrows()
        for col_index in range(1, len(row))
    ]
    min_value = min(value for _, _, value in data)
    max_value = max(value for _, _, value in data)

    return data_df.keys()[1:], data_df['country'], data,data_df, min_value, max_value

main_container = st.container()
options_col, chart_col = main_container.columns((page_ratio, 1-page_ratio))

graph_node=[]
graph_link=[]

with options_col:

    heatmap_type = ['country-company_type',
                    'country-company_lable',
                    'country-company_revenue',
                    'country-related2seafood']
    heatmap_choice = st.selectbox("选择热力图类型:", heatmap_type)

    xaxis_labels, yaxis_labels, data, data_df,min_value, max_value = process_heatmap_data(heatmap_choice)

    col1, col2 = st.columns(2)
    with col1:
        # 如果点击了“清除选中节点”按钮
        if st.button('Clear Selection'):
            st.session_state.all_chosen_nodes = []
            st.session_state.clear_signal = True  # 设置标志，指示需要忽略点击事件

    # 创建热力图
    heatmap = (
        HeatMap()
        .add_xaxis(list(xaxis_labels))
        .add_yaxis(
            series_name=heatmap_choice,
            yaxis_data=list(yaxis_labels),
            value=data,
            label_opts=opts.LabelOpts(is_show=False, position="inside"),
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title="HeatMap Example"),
            tooltip_opts=opts.TooltipOpts(is_show=True, formatter="{b0}: {c}"),
            yaxis_opts=opts.AxisOpts(
                axislabel_opts=opts.LabelOpts(font_size=10),
                position="right"),
            visualmap_opts=opts.VisualMapOpts(
                min_=min_value,
                max_=max_value,
                is_calculable=True,
                orient="horizontal",
                pos_left="center",
            )
        )
    )

    # 设置点击事件的JavaScript函数
    click_event_js = "function(params) {return params.data;}"

    # 渲染热力图并设置点击事件
    node_chosen = st_pyecharts(
        heatmap,
        events={"click": click_event_js},
        width="100%",
        height=700
    )
    
    # 当热力图被点击时，添加新节点到 session state
    if node_chosen and node_chosen not in st.session_state.all_chosen_nodes and st.session_state.clear_signal is False:
        st.session_state.all_chosen_nodes.append(node_chosen)

    # 如果清除信号被设置，则重置该信号
    if st.session_state.clear_signal:
        st.session_state.clear_signal = False

    st.write(st.session_state.all_chosen_nodes)

    with col2:
        # 如果点击了“添加到图表”按钮
        if st.button('Add to Graph'):
            temp_chosen_nodes = st.session_state.all_chosen_nodes.copy()
            
            # 清空 st.session_state.all_chosen_nodes
            st.session_state.all_chosen_nodes = []
            st.session_state.clear_signal = True
            
            # 遍历 node_chosen 列表
            for item in temp_chosen_nodes:
                if isinstance(item, list) and len(item) == 3:
                    col_idx, row_idx, number = item
                    if number != 0:
                        selected_country = data_df.iloc[row_idx, 0]  # 国家信息在第0列
                        selected_company_type = data_df.columns[col_idx + 1]  # +1 因为我们跳过了第一列，它通常是索引列

                        filtered_df = nodes[(nodes['country'] == selected_country) & (nodes['company_type'] == selected_company_type)]
                        graph_node.extend(filtered_df['id'].tolist())

        
        # 去除重复的节点ID
        graph_node = list(set(graph_node))
        # 打印结果
        print("graph_node:",graph_node)
