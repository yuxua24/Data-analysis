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


# 节点选择的集合
if 'nodes_chosen' not in st.session_state:
    st.session_state.nodes_chosen = set()

company_type = pd.read_csv('Dataset/country-company_type.csv')
company_lable = pd.read_csv('Dataset/country-company_lable.csv')
company_revenue = pd.read_csv('Dataset/country-company_revenue.csv')
related2seafood = pd.read_csv('Dataset/country-company_related2seafood.csv')


main_container = st.container()
options_col, chart_col = main_container.columns((page_ratio, 1-page_ratio))


with options_col:

    heatmap_type = ['country-company_type',
                    'country-company_lable',
                    'country-company_revenue',
                    'country-related2seafood']
    heatmap_choice = st.selectbox("选择热力图类型:", heatmap_type)

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
            title_opts=opts.TitleOpts(title="HeatMap Example"),
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

    node_chosen = st_pyecharts(
        heatmap,
        events={"click": click_event_js},
        width="100%",
        height=700
    )
    st.session_state.nodes_chosen.add(node_chosen[2])
    st.write(st.session_state.nodes_chosen)
