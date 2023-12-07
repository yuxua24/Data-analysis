import streamlit as st


st.set_page_config(page_title="FishEye", layout="wide",
                   page_icon=None, initial_sidebar_state="collapsed")

with st.container():
    col_select, col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 1, 1])

    with col_select:
        if 'sus_nodes' in st.session_state:
            select_box = st.selectbox(
                "Suspicious nodes", list(st.session_state['sus_nodes']))
        st.button('SHOW SIMILAR COMPANY')

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


st.markdown("---")

left_col, line_col, right_col = st.columns([1, 0.01, 1])

with left_col:
    st.subheader("Selected Node")
    st.button('REMOVE')

with line_col:
    st.markdown('<div style="height: 600px; width: 1px; background-color: #d3d3d3;"></div>',
                unsafe_allow_html=True)

with right_col:
    st.subheader("Similar Node")
    st.button('EXPAND')

st.markdown("---")
