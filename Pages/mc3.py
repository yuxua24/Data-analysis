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
page_ratio = st.slider('', min_value=0.0000, max_value=1.0,
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


main_container = st.container()
options_col, chart_col = main_container.columns((page_ratio, 1-page_ratio))


with options_col:

    heatmap_type = ['country-company_type',
                    'country-company_lable',
                    'country-company_revenue',
                    'country-related2seafood']
    heatmap_choice = st.selectbox("选择热力图类型:", heatmap_type)

    if st.button('Clear Selection'):
        # You can add any action you want to perform when the button is clicked
        st.session_state.all_chosen_nodes  =[]
        st.session_state.clear_signal = True  # 设置标志，指示需要忽略点击事件

    data = [[col_index - 1, row_index, row[col_index]]
            for row_index, row in company_type.iterrows()
            for col_index in range(1, len(row))] if heatmap_choice == 'country-company_type' else (
                [[col_index - 1, row_index, row[col_index]]
                 for row_index, row in company_lable.iterrows()
                 for col_index in range(1, len(row))] if heatmap_choice == 'country-company_lable' else (
                    [[col_index - 1, row_index, row[col_index]]
                     for row_index, row in company_revenue.iterrows()
                     for col_index in range(1, len(row))] if heatmap_choice == 'country-company_revenue' else (
                        [[col_index - 1, row_index, row[col_index]]
                            for row_index, row in related2seafood.iterrows()
                            for col_index in range(1, len(row))]
                    )
                )
    )

    # 计算数据的最小值和最大值
    min_value = min(value for _, _, value in data)
    max_value = max(value for _, _, value in data)

    # 创建热力图
    heatmap = (
        HeatMap()
        .add_xaxis(list(company_type.keys() if heatmap_choice == 'country-company_type' else (
            company_lable.keys() if heatmap_choice == 'country-company_lable' else (
                company_revenue.keys() if heatmap_choice == 'company_revenue' else (
                    related2seafood.keys()
                )
            )
        ))[1:])
        .add_yaxis(
            series_name=heatmap_choice,
            yaxis_data=list(company_revenue['country']),
            value=data,
            label_opts=opts.LabelOpts(is_show=False, position="inside"),
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title="HeatMap Example"),
            tooltip_opts=opts.TooltipOpts(is_show=True, formatter="{b0}: {c}"),
        )
        # 添加VisualMap组件
        .set_global_opts(
            tooltip_opts=opts.TooltipOpts(
                is_show=True, formatter="{b0}: {c}"),
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