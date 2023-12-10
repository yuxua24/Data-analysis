import streamlit as st
import pandas as pd


st.set_page_config(page_title="FishEye", layout="wide",
                   page_icon=None, initial_sidebar_state="collapsed")

nodes = pd.read_csv('Dataset/MC1/Nodes.csv')
links = pd.read_csv('Dataset/MC1/Links.csv')


def _divider_():
    return st.markdown("""
        <style>
        .divider {
            margin-top: 0px; /* 上边距 */
            margin-bottom: 0px; /* 下边距 */
            border-color: #FF0000; /* 设置分割线颜色 */
            width: 100%;
        }
        </style>
        <hr class="divider"/>
    """, unsafe_allow_html=True)


col1, mid_col, col2 = st.columns([2, 1, 5])

with col1:
    sus_nodes = st.selectbox("Suspicious Nodes", list(
        st.session_state['sus_nodes1']))
    top_k = st.number_input("Top K Most Suspicious Nodes",
                            min_value=1, max_value=100, value=1, step=1)
    st.markdown('---')
    slider1 = st.slider("Threshold of Community", 0.0, 1.0, step=0.01)
    slider1_2 = st.slider("Weight of Community", 0.0, 1.0,
                          step=0.01, key='slider1_2')
    _divider_()
    slider2 = st.slider("Threshold of Sigmod", 0.0, 1.0, step=0.01)
    slider2_2 = st.slider("Weight of Sigmod", 0.0, 1.0,
                          step=0.01, key='slider2_2')
    _divider_()
    slider3 = st.slider("Related To Location", 0.0, 1.0, step=0.01)
    _divider_()
    slider4 = st.slider("Threshold of Node", 0.0, 1.0, step=0.01)
    slider4_2 = st.slider("Weight of Node", 0.0, 1.0,
                          step=0.01, key='slider4_2')
    _divider_()
    slider5 = st.slider("Weight of Power-law", 0.0, 1.0, step=0.01)
    _divider_()
    slider6 = st.slider("Related To Government", 0.0, 1.0, step=0.01)


with col2:
    st.subheader("Suspicious Nodes")
