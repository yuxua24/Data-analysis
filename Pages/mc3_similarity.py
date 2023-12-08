import streamlit as st
import pandas as pd


st.set_page_config(page_title="FishEye", layout="wide",
                   page_icon=None, initial_sidebar_state="collapsed")

nodes1 = pd.read_csv('Dataset/MC3/nodes_1.csv')
nodes = pd.read_csv('Dataset/MC3/nodes.csv')
links = pd.read_csv('Dataset/MC3/links.csv')

show_similar = False
similar_nodes = set()

with st.container():
    col_select, col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 1, 1])

    with col1:
        slider1 = st.slider("Company Size", 0.0, 1.0, step=0.01)
        slider1_2 = st.slider("", -1.0, 0.0, value=0.0,
                              step=0.01, key='slider1_2')
    with col2:
        slider2 = st.slider("Country", 0.0, 1.0, step=0.01)
        slider2_2 = st.slider("", -1.0, 0.0, value=0.0,
                              step=0.01, key='slider2_2')
    with col3:
        slider3 = st.slider("Product Services", 0.0, 1.0, step=0.01)
        slider3_2 = st.slider("", -1.0, 0.0,  value=0.0,
                              step=0.01, key='slider3_2')
    with col4:
        slider4 = st.slider("Revenue", 0.0, 1.0, step=0.01)
        slider4_2 = st.slider("", -1.0, 0.0, value=0.0,
                              step=0.01, key='slider4_2')
    with col5:
        slider5 = st.slider("Same Staff", 0.0, 1.0, step=0.01)
        slider5_2 = st.slider("", -1.0, 0.0, value=0.0,
                              step=0.01, key='slider5_2')

    with col_select:
        node_chosen = st.selectbox(
            "Suspicious nodes", list(st.session_state['sus_nodes3']))
        top_k = st.number_input("Top K Similar Nodes",
                                min_value=1, max_value=100, value=1, step=1)

        def handle_show():
            global show_similar
            global similar_nodes
            show_similar = True
            cols = ['id','product_services','revenue_omu','type','country','company_type','company_size','clothing','furniture','groceries','logistics','machinery','management','metals','miscellaneous','pharmaceutical','plastics','food','seafood','missing']
            res = dict()
            for idx1, row1 in nodes1:
                if row1['id']==node_chosen:#先找到选择的节点
                    for idx, row in nodes1:
                        sum=0.0
                        for col in nodes1.columns:
                            sum+=0.0
                break

        st.button('SHOW SIMILAR NODES', on_click=handle_show)


st.markdown("---")

left_col, line_col, right_col = st.columns([1, 0.01, 1])

with left_col:
    st.subheader("Selected Node")

    def handle_remove():
        st.session_state['sus_nodes3'].discard(node_chosen)
    st.button('REMOVE', on_click=handle_remove)

    for index, row in nodes.iterrows():
        if row['id'] == node_chosen:
            details = ''
            for col in nodes.columns:
                st.markdown(
                    f"<span style='font-size: 20px; color: #000000;'><b>{col}:</b></span>", unsafe_allow_html=True)
                st.markdown(row[col])
            break


with line_col:
    st.markdown('<div style="height: 750px; width: 1px; background-color: #d3d3d3;"></div>',
                unsafe_allow_html=True)

with right_col:
    st.subheader("Similar Nodes")

    def handle_expand():
        pass
    st.button('EXPAND', on_click=handle_expand)


st.markdown("---")
