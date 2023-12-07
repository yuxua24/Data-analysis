import streamlit as st

st.set_page_config(page_title="FishEye", layout="wide",
                   page_icon=None, initial_sidebar_state="collapsed")

# Upper section with select box and two sets of sliders
with st.container():
    # Define columns for the select box and the first set of sliders
    col_select, col_space1, col1, col_space2, col2, col_space3, col3, col_space4, col4, col_space5, col5 = st.columns([
                                                                                                                      3, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2])

    with col_select:
        select_box = st.selectbox(
            "Choose Option", ["Option 1", "Option 2", "Option 3"])

    with col1:
        slider1 = st.slider("Company Size", 0.0, 1.0, step=0.01)
    with col2:
        slider2 = st.slider("Country", 0.0, 1.0, step=0.01)
    with col3:
        slider3 = st.slider("Product Services", 0.0, 1.0, step=0.01)
    with col4:
        slider4 = st.slider("Revenue", 0.0, 1.0, step=0.01)
    with col5:
        slider5 = st.slider("Same Staff", 0.0, 1.0, step=0.01)

    # Define columns for the second set of sliders, directly underneath the first set
    col_space6, col_space7, col6, col_space8, col7, col_space9, col8, col_space10, col9, col_space11, col10 = st.columns([
                                                                                                                         3, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2])

    with col_space6:
        st.button('SHOW SIMILAR COMPANY')
    # Adding a second set of sliders
    with col6:
        slider1_2 = st.slider("Company Size 2", -1.0, 0.0,
                              step=0.01, key='slider1_2')
    with col7:
        slider2_2 = st.slider("Country 2", -1.0, 0.0,
                              step=0.01, key='slider2_2')
    with col8:
        slider3_2 = st.slider("Product Services 2", -1.0,
                              0.0, step=0.01, key='slider3_2')
    with col9:
        slider4_2 = st.slider("Revenue 2", -1.0, 0.0,
                              step=0.01, key='slider4_2')
    with col10:
        slider5_2 = st.slider("Same Staff 2", -1.0, 0.0,
                              step=0.01, key='slider5_2')

# Divider line
st.markdown("---")

# Lower section divided into left and right with a vertical separator
left_col, line_col, right_col = st.columns([1, 0.01, 1])

with left_col:
    st.subheader("Selected Node")
with line_col:
    st.markdown('<div style="height: 1000px; width: 2px; background-color: #d3d3d3;"></div>',
                unsafe_allow_html=True)
with right_col:
    st.subheader("Similar Node")
